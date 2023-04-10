import queue
from PIL import Image, ImageOps
import pytesseract as pytess
import whisper
from notes import Note
import os
import threading
from globals import time_to_exit, to_transcribe_q, to_chatgpt_q


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


def transcribe_to_text(full_dir: str) -> str:
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


def to_text_and_place_on_chatgpt_q(full_dir: str) -> str:
    prepped_text = transcribe_to_text(full_dir)

    note = Note(prepped_text, full_dir)

    to_chatgpt_q.put(note)


# Forever watches for things put on the "to_transcribe_queue".
def to_transcribe_q_grabber():  # TODO: Put this in another python file
    # Forever loop as long as not time to exit
    while not time_to_exit.is_set():
        try:
            # Default is block=True, but helps with clarity. Blocks for 1 second, then checks if time to exit before
            # continuing to try and get the front queue item (blocking for 1 second again)
            full_dir = to_transcribe_q.get(block=True, timeout=1)
            file_name = os.path.basename(full_dir)

            # Make sure it is in fact a file that's there...
            if os.path.isfile(full_dir):
                # Start a thread to process from file to note
                to_note_thread = threading.Thread(target=to_text_and_place_on_chatgpt_q,
                                                  args=(full_dir,),
                                                  daemon=False,
                                                  name="to note thread")
                to_note_thread.start()
            # If it's not a file (folder or whatever) raise an exception
            else:
                raise Exception(f"File that was in queue for processing: {file_name} not a file")
        except queue.Empty:  # Pass only if queue.Empty, ensures other exceptions are not caught
            pass


# Only run if tests wanted
if __name__ == "__main__":
    text = run_whisper("C:\\Users\\Papis\\Documents\\~GitHub Projects\\AutoNote\\to process\\(0) 2023-03-30 22.20.53.590736.wav")
    print(text)
