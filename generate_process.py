import os
import time
import subprocess
import shlex
import logging
from text_to_audio import text_to_speech_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

ROOT_UPLOADS = "user_uploads"
DONE_FILE = "done.txt"
STATIC_REELS = "static/reels"


def ensure_done_file():
    if not os.path.exists(DONE_FILE):
        open(DONE_FILE, "w").close()


def read_done():
    with open(DONE_FILE, "r", encoding="utf-8") as f:
        return {x.strip() for x in f.readlines() if x.strip()}


def mark_done(folder):
    with open(DONE_FILE, "a", encoding="utf-8") as f:
        f.write(folder + "\n")


def process_folder(folder):
    logging.info(f"Processing: {folder}")

    folder_path = os.path.join(ROOT_UPLOADS, folder)
    desc_txt = os.path.join(folder_path, "desc.txt")

    # Read desc safely
    try:
        with open(desc_txt, "r", encoding="utf-8", errors="replace") as f:
            text = f.read().strip()
    except Exception as e:
        logging.error("Could not read desc.txt: %s", e)
        return False

    if not text:
        logging.error("desc.txt empty for %s", folder)
        return False

    # Generate TTS
    try:
        text_to_speech_file(text, folder)
    except Exception as e:
        logging.error("TTS failed for %s: %s", folder, e)
        return False

    # Create video using FFmpeg
    return make_reel(folder)


def make_reel(folder):
    folder_path = os.path.join(ROOT_UPLOADS, folder)
    input_txt = os.path.join(folder_path, "input.txt")
    audio_mp3 = os.path.join(folder_path, "audio.mp3")
    output_mp4 = os.path.join(STATIC_REELS, f"{folder}.mp4")

    # Convert Windows path to FFmpeg-safe
    input_txt = input_txt.replace("\\", "/")
    audio_mp3 = audio_mp3.replace("\\", "/")
    output_mp4 = output_mp4.replace("\\", "/")

    if not os.path.exists(input_txt):
        logging.error("Missing input.txt for %s", folder)
        return False

    if not os.path.exists(audio_mp3):
        logging.error("Missing audio.mp3 for %s", folder)
        return False

    cmd = (
        f"ffmpeg -y -f concat -safe 0 -i {shlex.quote(input_txt)} "
        f"-i {shlex.quote(audio_mp3)} "
        f"-vf \"scale=720:1280:force_original_aspect_ratio=decrease,"
        f"pad=720:1280:(ow-iw)/2:(oh-ih)/2:black\" "
        f"-c:v libx264 -preset ultrafast -pix_fmt yuv420p "
        f"-b:v 1M -maxrate 1M -bufsize 1M "
        f"-c:a aac -shortest -r 30 "
        f"{shlex.quote(output_mp4)}"
    )


    logging.info("Running FFmpeg...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("FFmpeg error: %s", result.stderr)
        return False

    logging.info("REEL CREATED: %s", output_mp4)
    return True


def start_processing():
    logging.info("Background worker started...")
    ensure_done_file()

    while True:
        done = read_done()
        folders = [
            f for f in os.listdir(ROOT_UPLOADS)
            if os.path.isdir(os.path.join(ROOT_UPLOADS, f))
        ]

        for folder in folders:
            if folder in done:
                continue

            ok = process_folder(folder)
            if ok:
                mark_done(folder)
            else:
                logging.warning("Failed for %s, will retry later", folder)

        time.sleep(3)
