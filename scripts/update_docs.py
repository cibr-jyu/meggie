import sys
import requests
import os
import tarfile
import zipfile
import json
import tempfile
from io import BytesIO
from pprint import pprint


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
    for file_path in list_files("meggie/actions"):
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


def get_package_metadata(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    response.raise_for_status()
    return response.json()


def read_configuration_json(temp_dir):
    # Search for configuration.json in the extracted files
    for root, dirs, files in os.walk(temp_dir):
        if "configuration.json" in files:
            config_path = os.path.join(root, "configuration.json")
            with open(config_path, "r") as config_file:
                return json.load(config_file)
    return {}


def extract_package(download_url, package_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        filename = os.path.basename(download_url)
        file_extension = os.path.splitext(filename)[1]
        if file_extension in [".gz", ".tar.gz", ".tgz"]:
            with tarfile.open(fileobj=BytesIO(package_data), mode="r:gz") as tar:
                tar.extractall(path=temp_dir)
        elif file_extension in [".whl", ".zip"]:
            with zipfile.ZipFile(BytesIO(package_data)) as zipf:
                zipf.extractall(path=temp_dir)
        else:
            raise ValueError("Unsupported package file format.")
        return read_configuration_json(temp_dir)


def search_pypi_packages(prefix):
    response = requests.get("https://pypi.org/simple/")
    response.raise_for_status()

    prefix_lower = prefix.lower().replace("_", "-")
    package_names = [
        line.split(">")[1].split("<")[0]
        for line in response.text.splitlines()
        if line.lower().startswith(f'<a href="/simple/{prefix_lower}')
    ]

    package_info = {}
    for package_name in package_names:
        try:
            metadata = get_package_metadata(package_name)
            version = metadata["info"]["version"]
            download_url = metadata["urls"][0]["url"]
            response = requests.get(download_url)
            response.raise_for_status()
            config_data = extract_package(download_url, response.content)

            package_info[package_name.replace("-", "_")] = {
                "version": version,
                "last_updated": metadata["releases"][version][0]["upload_time"].split(
                    "T"
                )[0],
                "name": config_data.get("name", ""),
                "author": config_data.get("author", ""),
            }
        except Exception as e:
            print(f"Could not fetch information about {package_name}: {e}")

    assert package_info
    return package_info


def create_markdown_table(plugin_metadata):
    headers = ["Plugin Name", "Version", "Last Updated", "Author", "Description"]
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for plugin, data in plugin_metadata.items():
        row = [
            plugin,
            data.get("version", ""),
            data.get("last_updated", ""),
            data.get("author", "").replace("|", "\\|"),
            data.get("name", "").replace("|", "\\|"),
        ]
        table += "| " + " | ".join(row) + " |\n"

    return table


if __name__ == "__main__":
    version = get_version()
    actions_raw = get_actions("raw")
    actions_spectrum = get_actions("spectrum")
    actions_epochs = get_actions("epochs")
    actions_evoked = get_actions("evoked")
    actions_tfr = get_actions("tfr")

    plugin_metadata = search_pypi_packages("meggie_")
    plugin_info = create_markdown_table(plugin_metadata)

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

        # Replace '{{PLUGIN_INFO}}' with the pypi information
        file_contents = file_contents.replace("{{PLUGIN_INFO}}", plugin_info)

        # Write the modified contents back to the file
        with open(file_path, "w") as f:
            f.write(file_contents)

    print("Updated the docs successfully.")
