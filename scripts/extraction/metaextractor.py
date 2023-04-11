import os
import sys
import argparse
from PIL import Image
from datetime import datetime
import json

def get_file_metadata(file_path):
    """
    Get metadata for file at given path.
    """
    # Get file name, size, and modified time
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

    # Get file type
    file_type = "Unknown"
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        file_type = "Image"
        # Get image dimensions
        try:
            with Image.open(file_path) as img:
                width, height = img.size
        except:
            width, height = None, None
    elif file_name.lower().endswith(('.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.mp3', '.mp4')):
        file_type = file_name.split('.')[-1].upper()
        width, height = None, None
    # Add more conditions for different file types here

    # Construct metadata dictionary
    metadata = {
        "file_path": file_path,
        "file_name": file_name,
        "file_size": file_size,
        "modified_time": str(modified_time),
        "file_type": file_type,
        "width": width,
        "height": height,
        # Add more metadata fields here
    }

    return metadata


def sort_directory(dir_path, sort_by, output_file=None):
    """
    Sort files in directory by given criteria.
    """
    # Get list of all files in directory
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    # Get metadata for each file
    metadata = [get_file_metadata(f) for f in files]

    # Sort files by given criteria
    if sort_by == "name":
        sorted_files = sorted(metadata, key=lambda x: x["file_name"])
    elif sort_by == "size":
        sorted_files = sorted(metadata, key=lambda x: x["file_size"])
    elif sort_by == "type":
        sorted_files = sorted(metadata, key=lambda x: x["file_type"])
    elif sort_by == "date":
        sorted_files = sorted(metadata, key=lambda x: x["modified_time"])
    # Add more sorting options here

    if output_file:
        with open(output_file, "w") as f:
            json.dump(sorted_files, f, indent=4)
    else:
        for f in sorted_files:
            print(f)


def main(args):
    parser = argparse.ArgumentParser(description="Sort files in directory by given criteria.")
    parser.add_argument("dir_path", type=str, help="The directory path to sort")
    parser.add_argument("--sort-by", type=str, default="name", choices=["name", "size", "type", "date"], help="The criteria to sort files by (default: name)")
    parser.add_argument("--output-file", type=str, help="The path to the output file to save metadata (in JSON format)")
    parsed_args = parser.parse_args(args)

    if not os.path.isdir(parsed_args.dir_path):
        print(f"Error: {parsed_args.dir_path} is not a directory.")
        return
    else:
        sort_directory(parsed_args.dir_path, parsed_args.sort_by, output_file=parsed_args.output_file)

if __name__ == "__main__":
    main(sys.argv[1:])
