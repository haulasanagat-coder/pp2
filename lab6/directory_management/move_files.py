import os
import shutil

os.makedirs("my_folder", exist_ok=True)
shutil.move("a.txt", "my_folder/a.txt")