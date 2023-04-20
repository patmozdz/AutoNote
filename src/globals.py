import queue
import os
import threading
import time
import keyboard
from keybinds import Keybind

# CONSTANTS:
# Directories
TO_PROCESS_DIR = os.path.join(os.getcwd(), "to process")
GARBAGE_DIR = os.path.join(os.getcwd(), "garbage")
# Default buffer durations (fix?)
BUFFER_MAX_DURATION = 5 * 60  # 5 minutes,
THREE_MIN = 3 * 60
ONE_MIN = 60
HALF_MIN = 30

# GLOBAL VARIABLES:
# To exit application
time_to_exit = threading.Event()
# Queues
to_transcribe_q = queue.Queue()  # A queue of file directories that need processing to text.  # TODO, make seperate queue for Pytesseract
to_chatgpt_q = queue.Queue()


# GLOBAL FUNCTIONS:
def set_time_to_exit():
    print("SETTING time_to_exit...")
    time_to_exit.set()


def show_keybinds():
    output = ""
    for category in current_keybinds.keys():
        for keybind in current_keybinds[category]:
            output += f"{keybind}\n"

    print(output)


def listen_for_keybinds(category: str, delay_after_press=0):
    while not time_to_exit.is_set():
        for keybind in current_keybinds[category]:
            if keyboard.is_pressed(keybind.get_key()):
                keybind.play_action()
                time.sleep(delay_after_press)
                break


current_keybinds = {
    # Set to none so that "make_keybinds" can instantiate
    "main": None,
    "recording": None
}


def find_keybind(name: str):
    for category in current_keybinds.keys():
        for keybind in current_keybinds[category]:
            if keybind.name == name:
                return keybind
    else:
        raise Exception("Tried to find a keybind that does not exist")


def make_keybinds():  # TODO: Change so it reads/writes to a file
    import audio_replay

    kb_exit = Keybind(name="Exit",
                      description="Exits the program",
                      default_key="q",
                      action=set_time_to_exit)

    kb_show_kbinds = Keybind(name="Show keybinds",
                             description="Shows all keybinds",
                             default_key="/",
                             action=show_keybinds)

    kb_save_slot_1 = Keybind(name="Save slot 1",
                             description="Saves last maximum duration seconds",
                             default_key="=",
                             action=audio_replay.start_save_thread,
                             action_params=(BUFFER_MAX_DURATION,))

    kb_save_slot_2 = Keybind(name="Save slot 2",
                             description="Saves last three minutes",
                             default_key="]",
                             action=audio_replay.start_save_thread,
                             action_params=(THREE_MIN,))

    kb_save_slot_3 = Keybind(name="Save slot 3",
                             description="Saves last one minute",
                             default_key="[",
                             action=audio_replay.start_save_thread,
                             action_params=(ONE_MIN,))

    # Add sets to "main" and "recording" so that later, find_keybind(name) can just search each set for the name
    current_keybinds["main"] = (kb_exit, kb_show_kbinds)
    current_keybinds["recording"] = (kb_save_slot_1, kb_save_slot_2, kb_save_slot_3)
