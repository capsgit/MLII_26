# gui.py
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from ttkthemes import ThemedTk

from engine import ModelManager, TranslateOptions, translate_path
from models import LANG_CHOICES, MODEL_MAP



# -------------------------------------------
# --------  I18N  --------------------------
# ------------------------------------------

I18N = {
    "es": {
        "title": "Notebook Translator (local)",
        "input": "Archivo o carpeta:",
        "file": "Archivo…",
        "folder": "Carpeta…",
        "from": "De:",
        "to": "A:",
        "select_lang": "— Selecciona idioma —",
        "log_ready": "Selecciona archivo/carpeta y elige idiomas.\n",
        "log_header": "\n== Traducción {from_} → {to_} ==\n",
        "log_input": "Entrada: {path}\n",
        "log_ok": "OK: {path}\n",
        "log_done": "Listo ✅\n",
        "log_cancelled": "Cancelado ❌\n",
        "log_error": "Error: {msg}\n",
        "opt_headings": "Traducir encabezados (# ...)",
        "opt_heur": "Heurística: traducir solo si parece alemán",
        "btn_translate": "Traducir",
        "btn_cancel": "Cancelar",
        "phase_wait": "Esperando selección…",
        "phase_loading": "Cargando modelo… (la primera vez puede tardar)",
        "phase_translating": "Traduciendo… ({i}/{total})",
        "phase_done": "Listo ✅",
        "phase_cancel": "Cancelado ❌",
        "warn_missing_path_title": "Falta ruta",
        "warn_missing_path_msg": "Selecciona un archivo o carpeta.",
        "err_model_title": "Modelo no configurado",
        "err_model_msg": "No hay modelo configurado para {from_}->{to_}.\nSe puede añadir al MODEL_MAP.",
        "warn_missing_lang_title": "Falta idioma",
        "warn_missing_lang_msg": "Selecciona un idioma en “A:”.",
        "phase_cancelling": "Cancelando…",
        "msg_error_title": "Error",
        "lbl_output": "Salida:",
        "runtime_cancelled": "Proceso cancelado por el usuario",
    },
    "en": {
        "title": "Notebook Translator (local)",
        "input": "File or folder:",
        "file": "File…",
        "folder": "Folder…",
        "from": "From:",
        "to": "To:",
        "select_lang": "— Select language —",
        "log_ready": "Select file/folder and choose languages.\n",
        "log_header": "\n== Translation {from_} → {to_} ==\n",
        "log_input": "Input: {path}\n",
        "log_ok": "OK: {path}\n",
        "log_done": "Done ✅\n",
        "log_cancelled": "Cancelled ❌\n",
        "log_error": "Error: {msg}\n",
        "opt_headings": "Translate headings (# ...)",
        "opt_heur": "Heuristic: translate only if it looks German",
        "btn_translate": "Translate",
        "btn_cancel": "Cancel",
        "phase_wait": "Waiting for input…",
        "phase_loading": "Loading model… (first time can take a while)",
        "phase_translating": "Translating… ({i}/{total})",
        "phase_done": "Done ✅",
        "phase_cancel": "Cancelled ❌",
        "warn_missing_path_title": "Missing path",
        "warn_missing_path_msg": "Select a file or folder.",
        "err_model_title": "Model not configured",
        "err_model_msg": "No model configured for {from_}->{to_}.\nAdd it to MODEL_MAP.",
        "warn_missing_lang_title": "Missing language",
        "warn_missing_lang_msg": "Select a language in “To:”.",
        "phase_cancelling": "Cancelling…",
        "msg_error_title": "Error",
        "lbl_output": "Output:",
        "runtime_cancelled": "Cancelled by user",
    },
    "de": {
        "title": "Notebook Translator (lokal)",
        "input": "Datei oder Ordner:",
        "file": "Datei…",
        "folder": "Ordner…",
        "from": "Von:",
        "to": "Nach:",
        "select_lang": "— Sprache auswählen —",
        "log_ready": "Bitte Datei/Ordner auswählen und Sprachen wählen.\n",
        "log_header": "\n== Übersetzung {from_} → {to_} ==\n",
        "log_input": "Eingabe: {path}\n",
        "log_ok": "OK: {path}\n",
        "log_done": "Fertig ✅\n",
        "log_cancelled": "Abgebrochen ❌\n",
        "log_error": "Fehler: {msg}\n",
        "opt_headings": "Überschriften (# ...) übersetzen",
        "opt_heur": "Heuristik: nur übersetzen, wenn es Deutsch ist",
        "btn_translate": "Übersetzen",
        "btn_cancel": "Abbrechen",
        "phase_wait": "Warte auf Auswahl…",
        "phase_loading": "Modell wird geladen… (beim ersten Mal dauert es)",
        "phase_translating": "Übersetze… ({i}/{total})",
        "phase_done": "Fertig ✅",
        "phase_cancel": "Abgebrochen ❌",
        "warn_missing_path_title": "Pfad fehlt",
        "warn_missing_path_msg": "Bitte Datei oder Ordner auswählen.",
        "err_model_title": "Modell nicht konfiguriert",
        "err_model_msg": "Kein Modell für {from_}->{to_} konfiguriert.\nBitte MODEL_MAP erweitern.",
        "warn_missing_lang_title": "Sprache fehlt",
        "warn_missing_lang_msg": "Bitte eine Zielsprache unter „Nach:“ wählen.",
        "phase_cancelling": "Wird abgebrochen…",
        "msg_error_title": "Fehler",
        "lbl_output": "Ausgabe:",
        "runtime_cancelled": "Vom Benutzer abgebrochen",
    },
}

class App:
    def __init__(self, root):
        self.root = root
        root.title("Notebook Translator (local)")
        root.geometry("1020x520+280+200")

        self.model_mgr = ModelManager()
        self.cancel_requested = False

        self.path_var = tk.StringVar()
        self.from_var = tk.StringVar(value="de")
        self.to_var = tk.StringVar(value="es")

        self.translate_headings = tk.BooleanVar(value=False)
        self.german_heuristic = tk.BooleanVar(value=True)

        self.ui_lang = tk.StringVar(value="de")
        self.to_choices_ui = []  # se rellenará en apply_i18n()

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill="both", expand=True)


        # Row: CB
        r0 = ttk.Frame(frm)
        r0.pack(fill="x", pady=(0, 6))

        ttk.Label(r0, text="UI:").pack(side="left")

        self.ui_cb = ttk.Combobox(r0, state="readonly", values=["Español (es)", "English (en)", "Deutsch (de)"])
        self.ui_cb.current(2)
        self.ui_cb.pack(side="left", padx=8)

        def on_ui_change(_evt=None):
            sel = self.ui_cb.current()
            self.ui_lang.set(["es", "en", "de"][sel])
            self.apply_i18n()

        self.ui_cb.bind("<<ComboboxSelected>>", on_ui_change)

        # Row: input
        r1 = ttk.Frame(frm)
        r1.pack(fill="x")
        self.lbl_input = ttk.Label(r1, text="")
        self.lbl_input.pack(side="left")
        ttk.Entry(r1, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=8)
        self.btn_file = ttk.Button(r1, text="", command=self.pick_file)
        self.btn_file.pack(side="left")

        self.btn_folder = ttk.Button(r1, text="", command=self.pick_dir)
        self.btn_folder.pack(side="left", padx=(6, 0))

        # Row: languages
        r3 = ttk.Frame(frm)
        r3.pack(fill="x", pady=(12,0))
        self.lbl_from = ttk.Label(r3, text="")
        self.lbl_from.pack(side="left")

        # self.from_cb = ttk.Combobox(r3, state="disabled", values=self.lang_values)
        self.from_cb = ttk.Combobox(r3, state="disabled", values=["Deutsch (de)"])
        self.from_cb.current(0)
        self.from_cb.pack(side="left", padx=8)

        self.lbl_to = ttk.Label(r3, text="")
        self.lbl_to.pack(side="left")

        self.to_cb = ttk.Combobox(r3, state="readonly", values=[])
        self.to_cb.pack(side="left", padx=8)

        # Row: options
        r4 = ttk.Frame(frm)
        r4.pack(fill="x", pady=(10,0))
        self.chk_headings = ttk.Checkbutton(
            r4,
            text="",
            variable=self.translate_headings
        )
        self.chk_headings.pack(side="left")

        self.chk_heur = ttk.Checkbutton(
            r4,
            text="",
            variable=self.german_heuristic
        )
        self.chk_heur.pack(side="left", padx=14)

        r_status = ttk.Frame(frm)
        r_status.pack(fill="x", pady=(12, 0))

        self.phase_lbl = ttk.Label(r_status, text="Esperando selección…", font=("Segoe UI", 11, "bold"))
        self.phase_lbl.pack(side="left")

        self.current_file_lbl = ttk.Label(r_status, text="", anchor="w")
        self.current_file_lbl.pack(side="left", padx=12, fill="x", expand=True)

        # Row: actions + progress
        r5 = ttk.Frame(frm)
        r5.pack(fill="x", pady=(12,0))
        self.btn = ttk.Button(r5, text="Traducir", command=self.start)
        self.btn.pack(side="left")
        self.cancel_btn = ttk.Button(r5, text="Cancelar", command=self.request_cancel)
        self.cancel_btn.pack(side="left", padx=(6, 0))
        self.cancel_btn.config(state="disabled")

        self.pb = ttk.Progressbar(r5, mode="determinate")
        self.pb.pack(side="left", fill="x", expand=True, padx=12)

        self.status = ttk.Label(r5, text="")
        self.status.pack(side="left")

        # Log
        self.log = tk.Text(frm, height=18)
        self.log.pack(fill="both", expand=True, pady=(12,0))

        self.log_msg("log_ready")
        self.apply_i18n()

    def append(self, msg: str):
        self.log.insert("end", msg)
        self.log.see("end")

    def build_to_choices(self):
        # Solo idiomas destino disponibles desde alemán (de)
        valid_to = sorted({to for (f, to) in MODEL_MAP.keys() if f == "de"})

        placeholder = (self.tr("select_lang"), "")
        choices = [placeholder]

        for name, code in LANG_CHOICES:
            if code in valid_to:
                choices.append((f"{name} ({code})", code))

        self.to_choices_ui = choices

    def request_cancel(self):
        self.cancel_requested = True
        self.phase_lbl.config(text=self.tr("phase_cancelling"))

    def pick_file(self):
        p = filedialog.askopenfilename(filetypes=[("Jupyter Notebook", "*.ipynb")])
        if p:
            self.path_var.set(p)

    def pick_dir(self):
        p = filedialog.askdirectory()
        if p:
            self.path_var.set(p)

    def get_langs(self):
        from_code = "de"
        idx = self.to_cb.current()
        to_code = self.to_choices_ui[idx][1] if idx >= 0 else ""
        return from_code, to_code

    def tr(self, key: str, **kwargs) -> str:
        lang = self.ui_lang.get()
        text = I18N.get(lang, I18N["en"]).get(key, key)
        return text.format(**kwargs)

    def apply_i18n(self):
        self.root.title(self.tr("title"))
        self.lbl_input.config(text=self.tr("input"))
        self.btn_file.config(text=self.tr("file"))
        self.btn_folder.config(text=self.tr("folder"))
        self.lbl_from.config(text=self.tr("from"))
        self.lbl_to.config(text=self.tr("to"))
        self.chk_headings.config(text=self.tr("opt_headings"))
        self.chk_heur.config(text=self.tr("opt_heur"))
        self.btn.config(text=self.tr("btn_translate"))
        self.cancel_btn.config(text=self.tr("btn_cancel"))

        # Si no está corriendo nada, mostramos estado idle en el idioma actual
        if self.btn["state"] != "disabled":
            self.phase_lbl.config(text=self.tr("phase_wait"))

        # Reconstruir SOLO destinos válidos + placeholder traducido
        prev_to_code = ""
        if self.to_choices_ui and self.to_cb.current() >= 0:
            prev_to_code = self.to_choices_ui[self.to_cb.current()][1]

        self.build_to_choices()

        self.to_cb["values"] = [label for (label, _code) in self.to_choices_ui]

        # Restaurar selección si existía
        def idx_for_code(code: str) -> int:
            for i, (_, c) in enumerate(self.to_choices_ui):
                if c == code:
                    return i
            return 0

        self.to_cb.current(idx_for_code(prev_to_code))

    def log_msg(self, key: str, **kwargs):
        self.append(self.tr(key, **kwargs))

    def start(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning(self.tr("warn_missing_path_title"), self.tr("warn_missing_path_msg"))
            return

        from_code, to_code = self.get_langs()
        if not to_code:
            messagebox.showwarning(self.tr("warn_missing_lang_title"), self.tr("warn_missing_lang_msg"))
            return

        self.btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.cancel_requested = False
        self.pb["value"] = 0
        self.status.config(text="")

        opts = TranslateOptions(
            translate_headings=self.translate_headings.get(),
            german_heuristic=self.german_heuristic.get()
        )

        inp = Path(path)

        self.log_msg("log_header", from_=from_code, to_=to_code)
        self.log_msg("log_input", path=inp)

        def progress(i, total, outp):
            if self.cancel_requested:
                raise RuntimeError(self.tr("runtime_cancelled"))

            def _ui():
                self.pb.stop()
                self.pb.config(mode="determinate")

                self.pb["maximum"] = max(total, 1)
                self.pb["value"] = i
                self.status.config(text=f"{i}/{total}")

                self.phase_lbl.config(text=self.tr("phase_translating", i=i, total=total))
                self.current_file_lbl.config(text=f'{self.tr("lbl_output")} {Path(outp).name}')

                self.log_msg("log_ok", path=outp)

            self.root.after(0, _ui)

        def worker():
            try:
                self.root.after(0, lambda: self.phase_lbl.config(text=self.tr("phase_loading")))
                self.root.after(0, lambda: self.current_file_lbl.config(text=""))
                self.root.after(0, lambda: self.pb.config(mode="indeterminate"))
                self.root.after(0, lambda: self.pb.start(10))

                translate_path(inp, from_code, to_code, None, opts, self.model_mgr, progress_cb=progress)

                self.root.after(0, lambda: self.phase_lbl.config(text=self.tr("phase_done")))
                self.root.after(0, lambda: self.log_msg("log_done"))
                self.root.after(0, lambda: self.pb.stop())
                self.root.after(0, lambda: self.pb.config(mode="determinate"))
            except RuntimeError:
                self.root.after(0, lambda: self.log_msg("log_cancelled"))
                self.root.after(0, lambda: self.phase_lbl.config(text=self.tr("phase_cancel")))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(self.tr("msg_error_title"), str(e)))
                self.root.after(0, lambda: self.phase_lbl.config(text="Error ❌"))
            finally:
                self.root.after(0, lambda: self.btn.config(state="normal"))
                self.root.after(0, lambda: self.cancel_btn.config(state="disabled"))

        threading.Thread(target=worker, daemon=True).start()


def main():
    root = ThemedTk(theme="breeze")
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
