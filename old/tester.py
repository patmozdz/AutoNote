import concurrent.futures
import whisper
import os
from pydub.utils import mediainfo


WHISP_MODEL = whisper.load_model("medium.en")
tester_path = os.path.join(os.getcwd(), "tester")
audio_files = [os.path.join(tester_path, file_name) for file_name in os.listdir(tester_path)]

info = mediainfo(audio_files[0])

for key, value in info.items():
    print(f"{key}: {value}")
