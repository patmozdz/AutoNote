from PIL import Image, ImageOps
import pytesseract as pytess
import whisper

SUPPORTED_AUD = {".mp4", ".mp3", ".wav", ".m4a"}
SUPPORTED_IMG = {".png", ".jpeg", ".tiff"}
WHISP_MODEL = whisper.load_model("medium.en")


def determine_type(file_name: str) -> str:
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



def run_pytess(file_name: str) -> str:
    with Image.open(file_name) as img:
        img = ImageOps.exif_transpose(img)  # If rotation is in exif, remove exif and rotate
        output_text = pytess.image_to_string(img, config="-l eng").strip()

    return output_text


def run_whisper(file_name: str) -> str:
    result = WHISP_MODEL.transcribe(file_name, fp16=False)  # fp16=False. Float precision can be set to only 16 if desired (bit faster), my CPU only supports 32 anyways so skip a warning check and just disable 16.
    output_text = result["text"].strip()

    return output_text


def preprocess(file_name) -> str:
    file_type = determine_type(file_name)
    if file_type in SUPPORTED_AUD:
        text = run_whisper(file_name)
    elif file_type in SUPPORTED_IMG:
        text = run_pytess(file_name)
    else:
        raise Exception(f"File: {file_name} with type {file_type} is not a supported file")

    return text
