from mastervariables import time_to_exit, to_chatgpt_q, GARBAGE_DIR, TO_PROCESS_DIR
import queue
from tempdir import TempDir
from notes import Note
import threading


def gpt_process_this(note: Note):
    # Replacing ChatGPT processing for now. Below should be non-daemon (so it's waited for)
    print(f"\n\n"
          f"\t\t---------------------------------------------------------\n"
          f"\t\t{note.get_og_file_len()} second file was prepared for ChatGPT with text:\n"
          f"\t\t---------------------------------------------------------\n\n\n"
          f"{note.get_og_text()}\n\n"
          f"Creation: {note.get_datetime_stamp()}\n\n\n\n\n")

    note.move_og_file_to(GARBAGE_DIR)


def pass_to_chatgpt():
    while not time_to_exit.is_set():
        try:
            # Default is block=True, but helps with clarity. Blocks for 1 second, then checks if time to exit before
            # continuing to try and get the front queue item (blocking for 1 second again)
            note = to_chatgpt_q.get(block=True, timeout=1)

            # New thread that's not daemon (so main waits for it to finish) that sets note object
            # self.gpt_notes attribute and self.topic attribute.
            gpt_processing_thread = threading.Thread(target=gpt_process_this,
                                                     daemon=False,
                                                     args=(note,),
                                                     name="gpt processing thread")
            gpt_processing_thread.start()

        except queue.Empty:  # Pass only if queue.Empty, ensures other exceptions are not caught
            pass

