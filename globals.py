import queue
import os
import threading
from keybinds import Keybind

# CONSTANTS:
# Directories
TO_PROCESS_DIR = os.path.join(os.getcwd(), "to process")  # TODO: Add gitignore to contents
GARBAGE_DIR = os.path.join(os.getcwd(), "garbage")  # TODO: Add gitignore to contents

# Default buffer durations (fix?)
BUFFER_MAX_DURATION = 5 * 60  # 5 minutes,
THREE_MIN = 3 * 60
ONE_MIN = 60
HALF_MIN = 30


# To exit application
time_to_exit = threading.Event()


def set_time_to_exit():
    print("SETTING time_to_exit...")
    time_to_exit.set()


# Queues
to_transcribe_q = queue.Queue()  # A queue of file directories that need processing to text.  # TODO, make seperate queue for Pytesseract
to_chatgpt_q = queue.Queue()


# Keybinds
kb_exit = Keybind(name="Exit",
                  description="Exits the program",
                  default_key="q",
                  action="set_time_to_exit")

kb_show_kbinds = Keybind(name="Show keybinds",
                         description="Shows all keybinds",
                         default_key="h",
                         action="show_keybinds")


kb_save_slot_1 = Keybind(name="Slot 1",
                         description="Saves last maximum duration seconds",
                         default_key="=",
                         action="start_save_thread",
                         action_params=(BUFFER_MAX_DURATION,))

kb_save_slot_2 = Keybind(name="Slot 2",
                         description="Saves last three minutes",
                         default_key="]",
                         action="start_save_thread",
                         action_params=(THREE_MIN,))

kb_save_slot_3 = Keybind(name="Slot 3",
                         description="Saves last one minute",
                         default_key="[",
                         action="start_save_thread",
                         action_params=(ONE_MIN,))

current_keybinds = {
    "main": [
        kb_exit,
        kb_show_kbinds
        ],

    "recording": [
        kb_save_slot_1,
        kb_save_slot_2,
        kb_save_slot_3
    ]
}


def show_keybinds():
    output = ""
    for category in current_keybinds:
        for keybind in category:
            output += f"{keybind}\n"

    print(output)
