from pathlib import Path
from yt_dlp import YoutubeDL
import time

# 🔧 Настройки
CHANNEL_URL = "https://www.youtube.com/channel/UCWiBh8LMDLi0sdL1bzRiEwg"  # замените на свой ID канала
COOKIES_FILE = "cookies.txt"  # путь к cookies
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# 🕒 Проверка завершения скачивания
def wait_for_file_complete(path, timeout=180):
    start_time = time.time()
    last_size = -1
    while time.time() - start_time < timeout:
        if path.exists():
            size = path.stat().st_size
            if size > 0 and size == last_size:
                return True
            last_size = size
        time.sleep(1)
    return False

# 🎧 Скачивание одного видео
def download_audio(video_id, retries=3):
    url = f"https://www.youtube.com/watch?v={video_id}"
    filename = DOWNLOAD_DIR / f"{video_id}.mp3"
    if filename.exists():
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(filename),
        "noplaylist": True,
        "nocheckcertificate": True,
        "cookies": COOKIES_FILE,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    for attempt in range(retries):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if wait_for_file_complete(filename):
                return
        except Exception as e:
            print(f"⚠️ Ошибка при скачивании {url}: {e}")
            time.sleep(1)

# 📋 Получение списка видео с канала
def get_video_ids_from_channel(channel_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": True,
        "cookies": COOKIES_FILE,
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        entries = result.get("entries", [])
        return [entry["id"] for entry in entries if entry.get("ie_key") == "Youtube"]

# 🚀 Основной запуск
def main():
    print("📌 Получаем список видео с канала...")
    video_ids = get_video_ids_from_channel(CHANNEL_URL)
    print(f"🔍 Найдено {len(video_ids)} видео")

    print("🎧 Скачиваем аудио...")
    for i, video_id in enumerate(video_ids, start=1):
        print(f"🎵 [{i}/{len(video_ids)}] {video_id}")
        download_audio(video_id)

if __name__ == "__main__":
    main()
