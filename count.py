import os
import sys

# For every file in the data folder ending in "long_desc_prs.txt", count the number of lines in the file and print the filename and the number of lines in the file.

# Get the path to the data folder
data_path = os.path.join(os.getcwd(), "data")

# Get a list of all the files in the data folder
files = os.listdir(data_path)

# Loop through the files
total_desc_lines = 0
total_rename_lines = 0
for file in files:
    # Check if the file ends in "long_desc_prs.txt"
    if file.endswith("long_desc_prs.txt"):
        # Get the path to the file
        file_path = os.path.join(data_path, file)
        # Open the file
        with open(file_path, "r") as f:
            # Count the number of lines
            num_lines = len(f.readlines())
            total_desc_lines += num_lines
            # Print the filename and the number of lines
            print(f"{file} has {num_lines} lines")

    if file.endswith("renamed_prs.txt"):
        # Get the path to the file
        file_path = os.path.join(data_path, file)
        # Open the file
        with open(file_path, "r") as f:
            # Count the number of lines
            num_lines = len(f.readlines())
            total_rename_lines += num_lines
            # Print the filename and the number of lines
            print(f"{file} has {num_lines} lines")

    with open("stats.txt", "w") as f:
        f.write(f"Total description lines: {total_desc_lines}\n")
        f.write(f"Total rename lines: {total_rename_lines}\n")
        f.write(f"Total lines: {total_desc_lines + total_rename_lines}\n")