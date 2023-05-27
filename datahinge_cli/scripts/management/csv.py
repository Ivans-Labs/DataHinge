"""
Module Name: csv_module

Description: This module provides functions for reading and writing data to/from CSV files.

Author: Sudo-Ivan
"""

import csv
import os
import sys
import argparse


def read_csv_file(file_path):
    """
    Read data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file.
    """
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def write_csv_file(file_path, data):
    """
    Write data to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data (list): A list of dictionaries, where each dictionary represents a row in the CSV file.

    Returns:
        None
    """
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def filter_csv_file(file_path, filter_function):
    """
    Filter data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        filter_function (function): A function that takes a dictionary representing a row in the CSV file as input and returns True or False.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file that passed the filter.
    """
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filter_function(row):
                data.append(row)
    return data


def sort_csv_file(file_path, key):
    """
    Sort data in a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        key (str): The key to sort the data by.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file sorted by the specified key.
    """
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = sorted(reader, key=lambda row: row[key])
    return data


def main(args):
    """
    Main function to handle command-line arguments and call appropriate functions.

    Args:
        args (list): List of command-line arguments.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="CSV Module")
    parser.add_argument("file_path", type=str, help="Path to the CSV file.")
    parser.add_argument("--filter", type=str, help="Filter function to apply to the CSV data.")
    parser.add_argument("--sort", type=str, help="Key to sort the CSV data by.")
    parsed_args = parser.parse_args(args)

    # Call the function to read the CSV file
    data = read_csv_file(parsed_args.file_path)

    if parsed_args.filter:
        # Call the function to filter the CSV data
        filter_function = eval(parsed_args.filter)
        data = filter_csv_file(parsed_args.file_path, filter_function)

    if parsed_args.sort:
        # Call the function to sort the CSV data
        data = sort_csv_file(parsed_args.file_path, parsed_args.sort)

    # Call the function to write the CSV file
    write_csv_file(parsed_args.file_path, data)


if __name__ == "__main__":
    main(sys.argv[1:])