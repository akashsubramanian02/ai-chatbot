import os
import tempfile

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def transcribe_audio(audio_bytes):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".webm"
    ) as temp_audio:

        temp_audio.write(audio_bytes)

        temp_path = temp_audio.name

    with open(
        temp_path,
        "rb"
    ) as file:

        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3"
        )

    return transcription.text