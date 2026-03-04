import whisper
from pathlib import Path

AUDIO_FOLDER = Path("C:/audios_klarmobil")
OUTPUT_FILE = Path("transcripciones.txt")

model = whisper.load_model("small")  # en CPU, small suele ir mejor

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for audio_file in AUDIO_FOLDER.glob("*.mp3"):
        print(f"Transcribiendo: {audio_file.name}")
        result = model.transcribe(str(audio_file), language="de", fp16=False)

        out.write(f"\n\n===== {audio_file.name} =====\n")
        out.write(result["text"])

print("✔ Transcripción completa. Archivo generado:", OUTPUT_FILE)
