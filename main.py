import os
import preper
from audioreplay import record_and_listen_for_input
import threading
from mastervariables import time_to_exit, to_chatgpt_q, TO_PROCESS_DIR, to_transcribe_q
import keyboard
from tochatgpt import to_chatgpt_q_grabber
from totranscribegrabber import to_transcribe_q_grabber


def main():
    # Start background recording thread
    background_rec_thread = threading.Thread(target=record_and_listen_for_input,
                                             daemon=True,
                                             name="background recording thread")
    background_rec_thread.start()

    # Start background thread that waits for items to show up in to_process, and then processes them into Notes objects
    wait_for_files_in_folder = threading.Thread(target=to_transcribe_q_grabber,
                                                daemon=True,
                                                name="wait to process thread")
    wait_for_files_in_folder.start()

    # Start background thread that constantly watches queue and passes notes to ChatGPT
    from_queue_to_gpt_thread = threading.Thread(target=to_chatgpt_q_grabber,
                                                daemon=True,
                                                name="pass to chatgpt thread")
    from_queue_to_gpt_thread.start()

    # Forever checks if keybind is pressed, if so sets "time_to_exit" event
    while not time_to_exit.is_set():
        if keyboard.is_pressed("q"):
            print("SETTING time_to_exit...")
            time_to_exit.set()

    # If q is pressed, exit loop and do the following
    print("Ending all threads (not waiting for daemon, waiting for others)...")
    # Wait until all non daemon threads exit. Basically this says daemon means is ok if stopped randomly
    for thread in threading.enumerate():
        # If statement should only be true if name == save thread or name == to note thread,
        # this makes sure all saving and file to note threads have time to finish before exiting main
        if thread != threading.current_thread() and not thread.daemon:
            print(f"Waiting for thread {thread} with name {thread.name} to end...")
            thread.join()
            print(f"Thread {thread} with name {thread.name} ended!")

    print("All non-daemon threads ended, ENDING!")


if __name__ == "__main__":
    main()
