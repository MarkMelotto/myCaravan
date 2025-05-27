import os
import shutil

# Set your target folder path
folder = r"c:\Users\markmelotto\PycharmProjects\myCaravan\zoe"

for filename in os.listdir(folder):
    if filename.endswith(".Cmd.txt"):
        old_path = os.path.join(folder, filename)
        new_filename = filename.replace(".Cmd.txt", ".csv")
        new_path = os.path.join(folder, new_filename)

        shutil.copyfile(old_path, new_path)
        print(f"Copied: {filename} -> {new_filename}")