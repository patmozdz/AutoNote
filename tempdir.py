import os


class TempDir:


  def __init__(self, new_dir):
    self.new_dir = new_dir
    self.old_dir = os.getcwd()


  def __enter__(self):
    os.chdir(self.new_dir)


  def __exit__(self, *args):
    os.chdir(self.old_dir)