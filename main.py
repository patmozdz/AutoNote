import os
import preper
from audioreplay import record_and_listen_for_input
import threading
from mastervariables import time_to_exit, to_chatgpt_q, TO_PROCESS_DIR, to_process_q
import keyboard
from tochatgpt import pass_to_chatgpt
import queue


def wait_to_process():  # TODO: Put this in another python file
    # Forever loop as long as not time to exit
    while not time_to_exit.is_set():
        try:
            # Default is block=True, but helps with clarity. Blocks for 1 second, then checks if time to exit before
            # continuing to try and get the front queue item (blocking for 1 second again)
            full_dir = to_process_q.get(block=True, timeout=1)
            file_name = os.path.basename(full_dir)

            # Make sure it is in fact a file that's there...
            if os.path.isfile(full_dir):
                # Start a thread to process from file to note
                to_note_thread = threading.Thread(target=preper.preprocess_to_note_and_place_in_queue,
                                                  args=(full_dir,),
                                                  daemon=False,
                                                  name="to note thread")
                to_note_thread.start()
            # If it's not a file (folder or whatever) raise an exception
            else:
                raise Exception(f"File that was in queue for processing: {file_name} not a file")
        except queue.Empty:  # Pass only if queue.Empty, ensures other exceptions are not caught
            pass


def main():
    # Start background recording thread
    background_rec_thread = threading.Thread(target=record_and_listen_for_input,
                                             daemon=True,
                                             name="background recording thread")
    background_rec_thread.start()

    # Start background thread that waits for items to show up in to_process, and then processes them into Notes objects
    wait_for_files_in_folder = threading.Thread(target=wait_to_process,
                                                daemon=True,
                                                name="wait to process thread")
    wait_for_files_in_folder.start()

    # Start background thread that constantly watches queue and passes notes to ChatGPT
    from_queue_to_gpt_thread = threading.Thread(target=pass_to_chatgpt,
                                                daemon=True,
                                                name="pass to chatgpt thread")
    from_queue_to_gpt_thread.start()

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
