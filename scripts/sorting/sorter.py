import os
import sys
import argparse
import shutil


def sort_files_by_extension(src_dir, dest_dir, overwrite=False, copy=False):
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

            try:
                if copy:
                    shutil.copy(src_file_path, dest_file_path)
                    print(f"Copied {filename} to {dest_subdir}")
                else:
                    shutil.move(src_file_path, dest_file_path)
                    print(f"Moved {filename} to {dest_subdir}")
            except Exception as e:
                print(f"Error moving/copying {filename}: {e}")


def main(args):
    parser = argparse.ArgumentParser(description="Sorts all files in the source directory by extension and moves or copies them to their respective subdirectories in the destination directory")
    parser.add_argument("src_dir", type=str, help="The source directory to sort")
    parser.add_argument("dest_dir", type=str, help="The destination directory to move/copy the sorted files to")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite files with the same name in the destination directory")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them to the destination directory")
    parsed_args = parser.parse_args(args)

    sort_files_by_extension(parsed_args.src_dir, parsed_args.dest_dir, parsed_args.overwrite, parsed_args.copy)


if __name__ == "__main__":
    main(sys.argv[1:])
