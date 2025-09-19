import os
import random

DIRECTORY = "KIIT/data"


def load_data(directory):
    # get all files and shuffle
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    random.shuffle(files)

    # loop and rename
    for i, filename in enumerate(files, start=1):  # start at 1
        old_path = os.path.join(directory, filename)

        # figure out which subfolder it belongs in
        batch_start = ((i - 1) // 100) * 100 + 1
        batch_end = batch_start + 99
        subfolder_name = f"KIIT_{batch_start}_{batch_end}"
        subfolder_path = os.path.join(directory, subfolder_name)

        # make subfolder if it doesn’t exist
        os.makedirs(subfolder_path, exist_ok=True)

        # new filename
        new_filename = f"KIIT_{i}.jpeg"
        new_path = os.path.join(subfolder_path, new_filename)

        # move+rename
        os.rename(old_path, new_path)


if __name__ == "__main__":
    load_data(DIRECTORY)

