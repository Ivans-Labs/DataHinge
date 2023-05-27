"""
Module Name: json_module

Description: This module provides functions for working with JSON data.

Author: Sudo-Ivan
"""

import json
import urllib.request


def read_json_file(file_path):
    """
    Read data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: A dictionary representing the JSON data.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def write_json_file(file_path, data):
    """
    Write data to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        data (dict): A dictionary representing the JSON data.

    Returns:
        None
    """
    with open(file_path, "w") as f:
        json.dump(data, f)


def read_json_url(url):
    """
    Read data from a JSON URL.

    Args:
        url (str): URL to the JSON data.

    Returns:
        dict: A dictionary representing the JSON data.
    """
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    return data


def main(args):
    """
    Main function to handle command-line arguments and call appropriate functions.

    Args:
        args (list): List of command-line arguments.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="JSON Module")
    parser.add_argument("file_path", type=str, help="Path to the JSON file.")
    parser.add_argument("--url", type=str, help="URL to the JSON data.")
    parsed_args = parser.parse_args(args)

    if parsed_args.url:
        # Call the function to read the JSON data from a URL
        data = read_json_url(parsed_args.url)
    else:
        # Call the function to read the JSON data from a file
        data = read_json_file(parsed_args.file_path)

    # Call the function to write the JSON data to a file
    write_json_file(parsed_args.file_path, data)


if __name__ == "__main__":
    main(sys.argv[1:])