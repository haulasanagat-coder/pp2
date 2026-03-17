import os

if not os.path.exists("my_folder"):
    os.mkdir("my_folder")

print(os.listdir())