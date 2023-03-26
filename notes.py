from datetime import datetime
import os
from pydub.utils import mediainfo


class Note:
    def __init__(self, og_text, og_file__dir, optional_prompt=None):  # TODO: Add word count (useful for ChatGPT max tokens)
        # Instantiate parameters
        self.og_text = og_text
        self.og_file__dir = og_file__dir

        # Not based on parameters
        self.datetime_stamp = datetime.now()
        self.topic = None
        self.gpt_notes = None
        # Not based on parameters, based on file
        self.og_file_name = os.path.basename(og_file__dir)
        try:
            self.og_file_info = mediainfo(og_file__dir)
            self.og_file_len = self.og_file_info.get("duration")
        except Exception as e:
            print(f"Could not get media info of {self.og_file_name} because of Exception: {e}")
            self.og_file_info = None
            self.og_file_len = None

    def move_og_file_to(self, to_directory):
        new_dir_and_name = os.path.join(to_directory, self.og_file_name)
        os.rename(self.og_file__dir, new_dir_and_name)  # TODO: Create so it's defensive function
        self.og_file__dir = new_dir_and_name

    def get_og_text(self):
        return self.og_text

    def get_datetime_stamp(self):
        return self.datetime_stamp

    def get_og_file_len(self):
        return self.og_file_len
