import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=API_KEY)


def text_to_speech_file(text, folder):
    output_path = os.path.join("user_uploads", folder, "audio.mp3")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logging.info("Requesting TTS...")

    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        text=text,
        model_id="eleven_turbo_v2_5",
        output_format="mp3_22050_32",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        )
    )

    with open(output_path, "wb") as f:
        for chunk in response:
            f.write(chunk)

    logging.info("Saved audio: %s", output_path)
    return output_path
