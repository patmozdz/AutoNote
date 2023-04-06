import queue
import threading
import os

# To exit application
time_to_exit = threading.Event()

# Queues
to_transcribe_q = queue.Queue()  # A queue of file directories that need processing to text.  # TODO, make seperate queue for Pytesseract
to_chatgpt_q = queue.Queue()


# CONSTANTS

# Directories
TO_PROCESS_DIR = os.path.join(os.getcwd(), "to process")  # TODO: Add gitignore to contents
GARBAGE_DIR = os.path.join(os.getcwd(), "garbage")  # TODO: Add gitignore to contents

# Recording
TODAYS_FILES_COUNTER = 0

BUFFER_MAX_DURATION = 5 * 60  # 5 minutes,
THREE_MIN = 3 * 60
ONE_MIN = 60
HALF_MIN = 30
