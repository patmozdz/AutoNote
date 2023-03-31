import pyaudio
import numpy as np
import wave
import keyboard
from collections import deque
import time
import os
import threading
from datetime import datetime
from mastervariables import *


# Constants
BUFFER_MAX_DURATION = 5 * 60  # 5 minutes
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024
# Constant time length
THREE_MIN = 3 * 60
ONE_MIN = 60
HALF_MIN = 30


# Sets up a deque with maxlen of 5 minutes worth of chunks (the deque consists of np arrays, each array is a chunk)
buffer = deque(maxlen=BUFFER_MAX_DURATION * RATE // CHUNK_SIZE)
buffer_lock = threading.Lock()


def record_audio():
    global buffer
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    while not time_to_exit.is_set():
        data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
        with buffer_lock:  # Lock so that the audio file cannot be saved while appending a new chunk
            buffer.append(data)
    else:  # Perform if time_to_exit is set to True
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Recording thread terminated.")


# Converts seconds of audio to number of audio chunks
def secs_to_num_chunks(secs: int) -> int:
    num_chunks = secs * RATE // CHUNK_SIZE

    return num_chunks


# Converts number of audio chunks to seconds of audio
def num_chunks_to_secs(num_chunks: int) -> int:
    secs = num_chunks * CHUNK_SIZE // RATE

    return secs


def save_audio(file_number: int, duration: int):
    # Lock so that if a new chunk is being appended to buffer, wait till it's appended.
    with buffer_lock:
        buffer_copy = tuple(buffer)

    # Decides if full requested amount of seconds can be saved (if recording long enough), prints message if not
    buffer_total_chunks = len(buffer_copy)
    wanted_chunks = secs_to_num_chunks(duration)  # TODO: Verify that // is good for this, possibly a chunk getting cut off and instead should use / then round up? (DEF DROPPING A CHUNK, LENGTH IS 29.952)
    if wanted_chunks > buffer_total_chunks:
        actual_duration = num_chunks_to_secs(buffer_total_chunks)
        print(f"Duration of {duration} seconds cannot be saved, "
              f"instead saving only the last {actual_duration} seconds...")
        chunks_to_process = buffer_total_chunks
    else:  # wanted_chunks <= buffer_total_chunks:
        chunks_to_process = wanted_chunks

    # Get current time, and name the file as file (number) current_datetime.
    # So for eg: (0) 12-1-2023 14.22.41.989934.wav
    curr_datetime = datetime.now()
    curr_datetime_str = curr_datetime.strftime("%Y-%m-%d %H.%M.%S.%f")
    file_name = f"({file_number}) {curr_datetime_str}.wav"

    # Set correct directory to save
    save_dir_with_name = os.path.join(TO_PROCESS_DIR, file_name)

    # Save file as .wav
    with wave.open(save_dir_with_name, "wb") as audio_file:
        # Audio setup stuff
        audio_file.setnchannels(CHANNELS)
        audio_file.setsampwidth(pyaudio.get_sample_size(FORMAT))
        audio_file.setframerate(RATE)

        # Traverse through last max_chunks of buffer_copy TODO: Same as above, make sure this isn't dropping a chunk (DEF DROPPING A CHUNK, LENGTH IS 29.952)
        for chunk in buffer_copy[buffer_total_chunks - chunks_to_process:]:
            audio_file.writeframes(chunk.tobytes())

    print(f"Request for {duration} seconds saved under file with name {file_name}!")
    to_transcribe_q.put(save_dir_with_name)  # Add path to queue so it's queued to change to text


def record_and_listen_for_input():
    # Start recording in the background
    recording_thread = threading.Thread(target=record_audio,
                                        daemon=True,
                                        name="recording thread")
    recording_thread.start()
    print("Recording... Press 's' to save the last 5 minutes of audio (d for 3, f for 1, g for .5).")

    # Listen for key presses until time to exit
    counter = 0
    while not time_to_exit.is_set():
        if keyboard.is_pressed("="):  # TODO: For the love of god turn this into a loop
            print("Saving last temp_MAXIMUM minutes...")
            time.sleep(.5)  # Ensures it saves while you're pressing the key (ending should be more accurate)

            # Start a separate thread for saving so that main loop can continue while a long file is saving
            save_thread = threading.Thread(target=save_audio,
                                           args=(counter, BUFFER_MAX_DURATION),
                                           daemon=False,
                                           name="save thread")
            save_thread.start()

            counter += 1
            time.sleep(.5)

        elif keyboard.is_pressed("]"):
            print("Saving last three minutes...")
            time.sleep(.5)  # Ensures it saves while you're pressing the key (ending should be more accurate)

            # Start a separate thread for saving so that main loop can continue while a long file is saving
            save_thread = threading.Thread(target=save_audio,
                                           args=(counter, THREE_MIN),
                                           daemon=False,
                                           name="save thread")
            save_thread.start()

            counter += 1
            time.sleep(.5)

        elif keyboard.is_pressed("["):
            print("Saving last one minute...")
            time.sleep(.5)  # Ensures it saves while you're pressing the key (ending should be more accurate)

            # Start a separate thread for saving so that main loop can continue while a long file is saving
            save_thread = threading.Thread(target=save_audio,
                                           args=(counter, ONE_MIN),
                                           daemon=False,
                                           name="save thread")
            save_thread.start()

            counter += 1
            time.sleep(.5)

        elif keyboard.is_pressed("'"):
            print("Saving last 30 seconds...")
            time.sleep(.5)  # Ensures it saves while you're pressing the key (ending should be more accurate)

            # Start a separate thread for saving so that main loop can continue while a long file is saving
            save_thread = threading.Thread(target=save_audio,
                                           args=(counter, HALF_MIN),
                                           daemon=False,
                                           name="save thread")
            save_thread.start()

            counter += 1
            time.sleep(.5)
