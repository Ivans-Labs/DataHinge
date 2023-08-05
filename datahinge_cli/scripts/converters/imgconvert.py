"""
Module Name: image_converter

Description: This script converts images from and to different formats.

Author: Sudo-Ivan
"""

import os
import sys
import argparse
from PIL import Image

def convert_image(input_path, output_path, output_format):
    """
    Convert an image to a specified format.

    Args:
        input_path (str): path to the input image file.
        output_path (str): path to the output image file.
        output_format (str): format to convert the image to.

    Returns:
        None
    """
    with Image.open(input_path) as img:
        img.save(output_path, format=output_format)
    print(f"Image converted to {output_format} format.")

def main(args):
    """
    Main function to handle command-line arguments and call appropriate functions.

    Args:
        args (list): list of command-line arguments.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Convert images to different formats.")
    parser.add_argument("input_path", type=str, help="Path to the input image file.")
    parser.add_argument("output_path", type=str, help="Path to the output image file.")
    parser.add_argument("output_format", type=str, help="Output image format.")
    parsed_args = parser.parse_args(args)

    # Check if input file exists
    if not os.path.isfile(parsed_args.input_path):
        print("Input file does not exist.")
        sys.exit(1)

    # Convert image to specified format
    convert_image(parsed_args.input_path, parsed_args.output_path, parsed_args.output_format)

if __name__ == "__main__":
    main(sys.argv[1:])