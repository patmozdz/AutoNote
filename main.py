import os
import preper
from tempdir import TempDir


def convert_and_display(folder="files"):

    new_path = os.path.join(os.getcwd(), folder)
    with TempDir(new_path):
        files = os.listdir()
        for file_name in files:
            if os.path.isfile(file_name):
                prepped_text = preper.preprocess(file_name)
                print(f"\t\t---------------------------\n"
                      f"\t\tFile with name: {file_name}\n"
                      f"\t\t---------------------------\n"
                      f"{prepped_text}\n\n\n")
            else:
                raise Exception(f"Non file: {file_name} found in {folder}")


convert_and_display()
