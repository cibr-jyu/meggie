import os
import sys

docs_dir = sys.argv[1]

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

if __name__ == '__main__':

    # parse version from setup.py
    with open("setup.py", "r") as f:
        lines = f.readlines()

    version = [
        line.split("=")[1].split(",")[0].strip("'") for line in lines if "version" in line
    ][0]

    # Search and replace the version in the md file
    for file_path in list_files(docs_dir):
        if not file_path.endswith('.md'):
            continue

        # Read the contents of the file
        with open(file_path, 'r') as f:
            file_contents = f.read()

        # Replace '{{VERSION}}' with the actual version
        file_contents = file_contents.replace('{{VERSION}}', version)

        # Write the modified contents back to the file
        with open(file_path, 'w') as f:
            f.write(file_contents)

    print("Updated the docs successfully.")
