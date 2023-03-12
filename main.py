from PIL import Image, ImageOps #TODO: update cudNN to 8.8 (currently 8700, as seen through print(torch.backends.cudnn.version()) virtual environment not inheriting PATH variables?
import pytesseract as pytess #TODO: Upgrade to Python 3.11.1 when Whisper becomes available on it
import whisper
import os

#Setup pytesseract and whisper:
model = whisper.load_model("medium.en")


def run_whisper(file_name: str) -> str: #TODO: Fix directory
#    with open("files/" + file_name, "r") as audio: #TODO: fix with (something fudged up)
    result = model.transcribe("files/" + file_name, fp16=False)  # fp16=False. Float precision can be set to only 16 if desired (bit faster), my CPU only supports 32 anyways so skip a warning check and just disable 16.
    output_text = result["text"].strip()

    return output_text


def run_pytess(file_name: str) -> str: #TODO: Fix directory
    with Image.open("files/" + file_name) as img:  # Perform operations to prime image before passed into pytess (use with Image.open() in this case?)
        img = ImageOps.exif_transpose(img)  # If rotation is in exif, return new image w/o orientation tag, rotated correctly
        output_text = pytess.image_to_string(img, config="-l eng").strip()

    return output_text


def determine_type(file_name: str) -> str:
    SUPPORTED_AUD = {".mp4", ".mp3", ".wav", ".m4a"}
    SUPPORTED_IMG = {".png", ".jpeg", ".tiff"}

    file_type = ""
    index = len(file_name) - 1
    while index >= 0:
        file_type = file_name[index] + file_type
        if file_name[index] == ".":
            break
        index -= 1
    else:
        raise Exception(f"File: {file_name} type {file_type} could not be determined")

    if file_type in SUPPORTED_AUD:
        return "audio"
    elif file_type in SUPPORTED_IMG:
        return "image"
    else:
        raise Exception(f"Not a supported file type: {file_type} for file: {file_name}")


files_dir = os.path.join(os.getcwd(), "files")
for file_name in os.listdir(files_dir):
    file_path = os.path.join(files_dir, file_name)

    if os.path.isfile(file_path):
        if determine_type(file_name) == "audio":
            print(f"\t\t---------------------------\n"
                  f"\t\tFile with name: {file_name}\n"
                  f"\t\t---------------------------\n"
                  f"{run_whisper(file_name)}\n\n\n")

        elif determine_type(file_name) == "image":
            print(f"\t\t---------------------------\n"
                  f"\t\tFile with name: {file_name}\n"
                  f"\t\t---------------------------\n"
                  f"{run_pytess(file_name)}\n\n\n")
    else:
        print("Non file found in directory")

