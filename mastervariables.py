import queue
import threading
import os

# This python file allows all threads to access this event
time_to_exit = threading.Event()

to_chatgpt_q = queue.Queue()

TO_PROCESS_DIR = os.path.join(os.getcwd(), "to process")  # TODO: Add gitignore to contents
to_transcribe_q = queue.Queue()  # A queue of file directories that need processing to text.  # TODO, make seperate queue for Pytesseract

GARBAGE_DIR = os.path.join(os.getcwd(), "garbage")  # TODO: Add gitignore to contents
