# engine.py
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Tuple, Optional

import torch
from transformers import MarianMTModel, MarianTokenizer

from models import MODEL_MAP

CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

LIST_RE = re.compile(r"^(\s*(?:[-*]|\d+\.)\s+)(.*)$")
HEADING_RE = re.compile(r"^(#{1,6}\s+)(.*)$")


@dataclass
class TranslateOptions:
    translate_headings: bool = False
    german_heuristic: bool = True


def split_text(text: str, max_chars: int = 1200):
    """
    Corta preservando separadores naturales:
    - primero intenta en doble salto (párrafo)
    - luego en salto simple
    - si no, corta a max_chars
    Devuelve chunks que incluyen el separador (cuando aplica), para poder hacer "".join().
    """
    if len(text) <= max_chars:
        return [text]

    parts = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)

        cut = text.rfind("\n\n", start, end)
        if cut != -1 and cut > start + 200:
            cut += 2
        else:
            cut = text.rfind("\n", start, end)
            if cut != -1 and cut > start + 200:
                cut += 1
            else:
                cut = end

        parts.append(text[start:cut])
        start = cut

    return parts


def looks_german(s: str) -> bool:
    s_low = " " + s.lower() + " "
    hits = 0
    hits += sum(w in s_low for w in [" der ", " die ", " das ", " und ", " nicht ", " ist ", " mit ", " auf ", " für "])
    hits += sum(ch in s for ch in "äöüß")
    return hits >= 1


def should_translate_line(line: str, *, opts: TranslateOptions) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    if stripped.startswith("#"):
        return opts.translate_headings and (looks_german(stripped) if opts.german_heuristic else True)

    if stripped.startswith(">"):
        return True

    if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s", stripped):
        return True

    if HTML_TAG_RE.search(stripped) and len(stripped) < 200:
        return False

    if not opts.german_heuristic:
        return True

    return looks_german(stripped)


class ModelManager:
    """Cachea modelos/tokenizers por (from,to) para no recargar."""
    def __init__(self):
        self._cache: Dict[Tuple[str, str], Tuple[MarianTokenizer, MarianMTModel, str]] = {}

    def get_translator(self, from_lang: str, to_lang: str) -> Callable[[str], str]:
        key = (from_lang, to_lang)
        if key not in MODEL_MAP:
            raise ValueError(f"No hay modelo configurado para {from_lang}->{to_lang}")

        model_name = MODEL_MAP[key]

        if key not in self._cache:
            tok = MarianTokenizer.from_pretrained(model_name)

            mdl, info = MarianMTModel.from_pretrained(model_name, output_loading_info=True)

            missing = info.get("missing_keys", []) or []
            unexpected = info.get("unexpected_keys", []) or []
            if missing or unexpected:
                print(f"[WARN] Modelo {model_name}: missing={len(missing)}, unexpected={len(unexpected)}")

            mdl.eval()
            device = "cuda" if torch.cuda.is_available() else "cpu"
            mdl.to(device)

            self._cache[key] = (tok, mdl, device)

        tok, mdl, device = self._cache[key]

        def _translate(text: str) -> str:
            chunks = split_text(text, max_chars=1200)
            outs = []

            with torch.no_grad():
                for ch in chunks:
                    batch = tok([ch], return_tensors="pt", truncation=True).to(device)
                    gen = mdl.generate(
                        **batch,
                        num_beams=5,
                        length_penalty=1.0,
                        no_repeat_ngram_size=3,
                        max_length=512,
                        early_stopping=True,
                    )
                    outs.append(tok.decode(gen[0], skip_special_tokens=True))

            # clave: NO meter saltos artificiales; split_text ya preserva separadores
            return "".join(outs)

        return _translate


def translate_markdown(md: str, translate_fn: Callable[[str], str], opts: TranslateOptions) -> str:
    # 1) Congelar fences
    fences = []

    def stash_fence(m):
        fences.append(m.group(0))
        return f"@@@FENCE_{len(fences)-1}@@@"

    tmp = CODE_FENCE_RE.sub(stash_fence, md)

    out = []
    buf = []

    def protect_inline(s: str):
        """
        Protege cosas que NO deben traducirse o que rompen al modelo:
        - imágenes y links markdown completos
        - inline code `...`
        - tags HTML
        Usa placeholders con separadores para que el tokenizador no los pegue.
        """
        protected = []

        def stash(m):
            protected.append(m.group(0))
            idx = len(protected) - 1
            return f" ⟦P{idx}⟧ "

        s2 = s
        s2 = MD_IMAGE_RE.sub(stash, s2)
        s2 = MD_LINK_RE.sub(stash, s2)
        s2 = INLINE_CODE_RE.sub(stash, s2)
        s2 = HTML_TAG_RE.sub(stash, s2)
        return s2, protected

    def restore_inline(s: str, protected):
        for i, p in enumerate(protected):
            s = s.replace(f"⟦P{i}⟧", p)
        return s

    def flush_buf():
        nonlocal buf
        if not buf:
            return

        lines = buf
        buf = []

        # Si nada pinta a alemán y la heurística está activa, no tocar.
        if not any(should_translate_line(ln, opts=opts) for ln in lines):
            out.append("\n".join(lines))
            return

        out_lines = []
        para_acc = []

        def flush_paragraph():
            nonlocal para_acc
            if not para_acc:
                return
            block = "\n".join(para_acc)
            para_acc = []
            block2, prot = protect_inline(block)
            tr = translate_fn(block2)
            tr = restore_inline(tr, prot)
            out_lines.append(tr)

        for line in lines:
            if line.strip() == "":
                flush_paragraph()
                out_lines.append("")
                continue

            # heading
            m = HEADING_RE.match(line)
            if m:
                flush_paragraph()
                prefix, title = m.group(1), m.group(2)
                if opts.translate_headings and (looks_german(title) if opts.german_heuristic else True):
                    title2, prot = protect_inline(title)
                    title_tr = restore_inline(translate_fn(title2), prot)
                    out_lines.append(prefix + title_tr)
                else:
                    out_lines.append(line)
                continue

            # list item
            m = LIST_RE.match(line)
            if m:
                flush_paragraph()
                prefix, body = m.group(1), m.group(2)
                if should_translate_line(body, opts=opts):
                    body2, prot = protect_inline(body)
                    body_tr = restore_inline(translate_fn(body2), prot)
                    out_lines.append(prefix + body_tr)
                else:
                    out_lines.append(line)
                continue

            # normal line -> paragraph accumulator
            para_acc.append(line)

        flush_paragraph()
        out.append("\n".join(out_lines))

    # 2) recorrer líneas y agrupar en bloques
    for line in tmp.splitlines(keepends=False):
        if "@@@FENCE_" in line:
            flush_buf()
            out.append(line)
            continue

        if line.strip() == "":
            flush_buf()
            out.append("")
            continue

        buf.append(line)

    flush_buf()

    translated_all = "\n".join(out)

    # 3) restaurar fences
    for i, fence in enumerate(fences):
        translated_all = translated_all.replace(f"@@@FENCE_{i}@@@", fence)

    return translated_all


def translate_notebook(in_path: Path, out_path: Path, translate_fn: Callable[[str], str], opts: TranslateOptions):
    nb = json.loads(in_path.read_text(encoding="utf-8"))

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            md = "".join(cell.get("source", []))
            md_out = translate_markdown(md, translate_fn, opts)
            cell["source"] = [md_out]

    out_path.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding="utf-8")


def translate_path(
    input_path: Path,
    from_lang: str,
    to_lang: str,
    out_dir: Optional[Path],
    opts: TranslateOptions,
    model_mgr: ModelManager,
    progress_cb: Optional[Callable[[int, int, str], None]] = None,
):
    input_path = Path(input_path)
    translate_fn = model_mgr.get_translator(from_lang, to_lang)

    if input_path.is_file() and input_path.suffix.lower() == ".ipynb":
        out_path = input_path.with_name(input_path.stem + f".{to_lang}.ipynb")
        translate_notebook(input_path, out_path, translate_fn, opts)
        if progress_cb:
            progress_cb(1, 1, str(out_path))
        return [out_path]

    if input_path.is_dir():
        nb_files = [
            p for p in sorted(input_path.rglob("*.ipynb"))
            if not p.stem.endswith(f".{to_lang}")
        ]
        total = len(nb_files)

        if total == 0:
            raise ValueError(f"No encontré notebooks .ipynb dentro de: {input_path}")

        outputs = []
        for i, nb in enumerate(nb_files, start=1):
            out_path = nb.with_name(f"{nb.stem}.{to_lang}.ipynb")
            translate_notebook(nb, out_path, translate_fn, opts)
            outputs.append(out_path)
            if progress_cb:
                progress_cb(i, total, str(out_path))

        return outputs
