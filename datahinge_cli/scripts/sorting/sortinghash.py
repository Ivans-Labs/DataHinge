import os
import sys
import argparse
import shutil
import hashlib
import time


def sort_files_by_extension(src_dir, dest_dir, overwrite=False, copy=False, hash=False, preserve_timestamps=False):
    """
    Recursively sorts all files in the source directory by extension and moves or copies them to their respective
    subdirectories in the destination directory.
    """
    if not os.path.isdir(src_dir):
        print(f"Error: {src_dir} is not a directory.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    # Initialize a dictionary to store the original and sorted hash values of each file
    hash_values = {}

    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            src_file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()

            # Create the subdirectory for the file extension if it doesn't exist
            dest_subdir = os.path.join(dest_dir, file_ext[1:])
            if not os.path.isdir(dest_subdir):
                os.mkdir(dest_subdir)

            dest_file_path = os.path.join(dest_subdir, filename)

            # Check if file with same name already exists in destination directory
            if os.path.exists(dest_file_path) and not overwrite:
                print(f"File {filename} already exists in {dest_subdir}")
                continue

            # Calculate the hash value of the original file if hash option is enabled
            if hash:
                with open(src_file_path, "rb") as f:
                    hash_object = hashlib.sha256()
                    while True:
                        data = f.read(65536)
                        if not data:
                            break
                        hash_object.update(data)
                    original_hash = hash_object.hexdigest()
                    hash_values[src_file_path] = {"original": original_hash}

            try:
                if copy:
                    shutil.copy(src_file_path, dest_file_path)
                    print(f"Copied {filename} to {dest_subdir}")
                else:
                    shutil.move(src_file_path, dest_file_path)
                    print(f"Moved {filename} to {dest_subdir}")
            except Exception as e:
                print(f"Error moving/copying {filename}: {e}")
                continue

            # Calculate the hash value of the sorted file if hash option is enabled
            if hash:
                with open(dest_file_path, "rb") as f:
                    hash_object = hashlib.sha256()
                    while True:
                        data = f.read(65536)
                        if not data:
                            break
                        hash_object.update(data)
                    sorted_hash = hash_object.hexdigest()
                    hash_values[src_file_path]["sorted"] = sorted_hash

            # Preserve the original file's timestamps if preserve_timestamps option is enabled
            if preserve_timestamps:
                os.utime(dest_file_path, (os.path.getatime(src_file_path), os.path.getmtime(src_file_path)))

    # Save the hash values to a log file if hash option is enabled
    if hash:
        log_file_path = os.path.join(dest_dir, "hash_log.txt")
        with open(log_file_path, "w") as f:
            for file_path, values in hash_values.items():
                f.write(f"File: {file_path}\n")
                f.write(f"Original hash: {values['original']}\n")
                f.write(f"Sorted hash: {values['sorted']}\n")
                f.write("\n")
    
    # Print a summary of the sorting process
    print("\nSorting complete!\n")
    if hash:
        print(f"Hash log saved to {log_file_path}\n")
    
def main(args):
    parser = argparse.ArgumentParser(description="Sorts all files in the source directory by extension and moves or copies them to their respective subdirectories in the destination directory")
    parser.add_argument("src_dir", type=str, help="The source directory to sort")
    parser.add_argument("dest_dir", type=str, help="The destination directory to move/copy the sorted files to")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite files with the same name in the destination directory")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them to the destination directory")
    parser.add_argument("--hash", action="store_true", help="Calculate hash values of files before and after sorting")
    parser.add_argument("--preserve-timestamps", action="store_true", help="Preserve the timestamps of the original files")
    parsed_args = parser.parse_args(args)

    sort_files_by_extension(parsed_args.src_dir, parsed_args.dest_dir, parsed_args.overwrite, parsed_args.copy, parsed_args.hash, parsed_args.preserve_timestamps)

if __name__ == "__main__":
    main(sys.argv[1:])
