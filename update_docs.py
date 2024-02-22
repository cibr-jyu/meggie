import os
import sys
import json

docs_dir = sys.argv[1]


def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def get_version():
    with open("setup.py", "r") as f:
        lines = f.readlines()
    version = [
        line.split("=")[1].split(",")[0].strip("'")
        for line in lines
        if "version" in line
    ][0]
    return version


def get_actions(prefix):
    actions = []
    for file_path in list_files('meggie/actions'):
        if not file_path.split("/")[-1] == "configuration.json":
            continue

        with open(file_path, "r") as f:
            config = json.load(f)

        name = config["name"]
        key = config["id"]
        description = config.get("description", "")

        actions.append((key, name, description))

    # Sort the list by the first element of each tuple
    sorted_actions = sorted(actions, key=lambda x: x[0])

    # Create the formatted string
    formatted_strings = []
    for action in sorted_actions:
        if not action[1]:
            continue

        if not action[0].startswith(prefix):
            continue

        if action[0].endswith("_info"):
            continue

        title = f"{action[1]} ({action[0]})"
        desc = action[2] or "To be added."
        formatted_strings.append(f"### {title}\n\n{desc}\n")

    # Join all formatted strings into one final string
    final_actions_output = "\n".join(formatted_strings)
    return final_actions_output


if __name__ == "__main__":

    version = get_version()
    actions_raw = get_actions("raw")
    actions_spectrum = get_actions("spectrum")
    actions_epochs = get_actions("epochs")
    actions_evoked = get_actions("evoked")
    actions_tfr = get_actions("tfr")

    for file_path in list_files(docs_dir):
        if not file_path.endswith(".md"):
            continue

        # Read the contents of the file
        with open(file_path, "r") as f:
            file_contents = f.read()

        # Replace '{{VERSION}}' with the actual version
        file_contents = file_contents.replace("{{VERSION}}", version)

        # Replace '{{ACTIONS_RAW}}' with the extrated action information
        file_contents = file_contents.replace("{{ACTIONS_RAW}}", actions_raw)

        # Replace '{{ACTIONS_SPECTRUM}}' with the extrated action information
        file_contents = file_contents.replace("{{ACTIONS_SPECTRUM}}", actions_spectrum)

        # Replace '{{ACTIONS_EPOCHS}}' with the extrated action information
        file_contents = file_contents.replace("{{ACTIONS_EPOCHS}}", actions_epochs)

        # Replace '{{ACTIONS_EVOKED}}' with the extrated action information
        file_contents = file_contents.replace("{{ACTIONS_EVOKED}}", actions_evoked)

        # Replace '{{ACTIONS_TFR}}' with the extrated action information
        file_contents = file_contents.replace("{{ACTIONS_TFR}}", actions_tfr)

        # Write the modified contents back to the file
        with open(file_path, "w") as f:
            f.write(file_contents)

    print("Updated the docs successfully.")
