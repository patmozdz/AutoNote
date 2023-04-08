from globals import time_to_exit, to_transcribe_q
import os
import queue
import preper
import threading


# Forever watches for things put on the "to_transcribe_queue".
def to_transcribe_q_grabber():  # TODO: Put this in another python file
    # Forever loop as long as not time to exit
    while not time_to_exit.is_set():
        try:
            # Default is block=True, but helps with clarity. Blocks for 1 second, then checks if time to exit before
            # continuing to try and get the front queue item (blocking for 1 second again)
            full_dir = to_transcribe_q.get(block=True, timeout=1)
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
