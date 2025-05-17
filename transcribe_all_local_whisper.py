import os
from pathlib import Path
import whisper

# Папка с аудиофайлами
AUDIO_DIR = Path("downloads")
AUDIO_DIR.mkdir(exist_ok=True)

# Модель Whisper
model = whisper.load_model("base")

# Проходим по всем .mp3
for file in AUDIO_DIR.glob("*.mp3"):
    print(f"🎙️ Распознаём: {file.name}")
    result = model.transcribe(str(file), language="ru")
    
    # Сохраняем в .txt
    txt_path = file.with_suffix(".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"✅ Готово: {txt_path.name}")
