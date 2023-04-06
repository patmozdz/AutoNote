from mastervariables import time_to_exit, BUFFER_MAX_DURATION, THREE_MIN, ONE_MIN, HALF_MIN
from audioreplay import start_save_thread  # TODO: FIX CIRCULAR IMPORT (This one imports the other one, and the other one on like line 5 imports this one. How to do it with how it's currently set up?
from keybinds import Keybind


def show_keybinds():
    output = ""
    for category in DEFAULT_KEYBINDS:
        for keybind in category:
            output += f"{keybind}\n"

    print(output)


def set_time_to_exit():
    print("SETTING time_to_exit...")
    time_to_exit.set()


DEFAULT_KEYBINDS = {
    "main": [
        Keybind("Exit", "Exits the program", "q", set_time_to_exit),
        Keybind("Show Keybinds", "Shows all keybinds", "h", show_keybinds)
        ],

    "recording": [
        Keybind("Save", "Saves last maximum duration seconds", "=", start_save_thread, (BUFFER_MAX_DURATION,)),
        Keybind("Save", "Saves last three minutes", "]", start_save_thread, (THREE_MIN,)),
        Keybind("Save", "Saves last one minute", "[", start_save_thread, (ONE_MIN,)),
        Keybind("Save", "Saves the last 30 seconds", "'", start_save_thread, (HALF_MIN,))
    ]
}
