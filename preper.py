# TODO: MERGE THIS WITH TOTRANSCRIBE GRABBER

from PIL import Image, ImageOps
import pytesseract as pytess
import whisper
from notes import Note
from globals import to_chatgpt_q
import os
import threading

SUPPORTED_AUD = {".mp4", ".mp3", ".wav", ".m4a"}
SUPPORTED_IMG = {".png", ".jpeg", ".tiff"}
WHISP_MODEL = whisper.load_model("medium.en")
run_whisper_lock = threading.Lock()  # Lock needed because whisper cannot run concurrently on multiple threads


def determine_type(full_dir: str) -> str:  # TODO: Can I just get format_name from note.mediainfo?
    file_name = os.path.basename(full_dir)

    for supported_type in SUPPORTED_AUD.union(SUPPORTED_IMG):
        if file_name.endswith(supported_type):

            return supported_type
    else:
        file_type = ""
        index = len(file_name) - 1
        while index >= 0:
            file_type = file_name[index] + file_type
            if file_name[index] == ".":

                return file_type
            index -= 1
        else:
            raise Exception(f"File: {file_name} type could not be determined")


def run_pytess(full_dir: str) -> str:
    file_name = os.path.basename(full_dir)
    print(f"Translating {file_name} with pytesseract...")

    with Image.open(full_dir) as img:
        img = ImageOps.exif_transpose(img)  # If rotation is in exif, remove exif and rotate
        output_text = pytess.image_to_string(img, config="-l eng").strip()

    print(f"Translated {file_name} using pytesseract!")
    return output_text


def run_whisper(full_dir: str) -> str:
    file_name = os.path.basename(full_dir)
    print(f"Translating {file_name} with whisper...")

    result = WHISP_MODEL.transcribe(full_dir, fp16=False)  # fp16=False. Float precision can be set to only 16 if desired (bit faster), my CPU only supports 32 anyways so skip a warning check and just disable 16.
    output_text = result["text"].strip()

    print(f"Translated {file_name} using whisper!")
    return output_text


def preprocess(full_dir: str) -> str:
    file_name = os.path.basename(full_dir)

    file_type = determine_type(full_dir)
    if file_type in SUPPORTED_AUD:
        with run_whisper_lock:
            output_text = run_whisper(full_dir)
    elif file_type in SUPPORTED_IMG:
        output_text = run_pytess(full_dir)
    else:
        raise Exception(f"File: {file_name} with type {file_type} is not a supported file")

    return output_text


def preprocess_to_note_and_place_in_queue(full_dir: str) -> str:
    prepped_text = preprocess(full_dir)

    note = Note(prepped_text, full_dir)

    to_chatgpt_q.put(note)


# Only run if tests wanted
if __name__ == "__main__":
    text = run_whisper("C:\\Users\\Papis\\Documents\\~GitHub Projects\\AutoNote\\to process\\(0) 2023-03-30 22.20.53.590736.wav")
    print(text)
