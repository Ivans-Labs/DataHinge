import os
import sys
import argparse
import shutil


def sort_files_by_extension(src_dir, dest_dir):
    """
    Sorts all files in the source directory by extension and moves them to their respective
    subdirectories in the destination directory.
    """
    if not os.path.isdir(src_dir):
        print(f"Error: {src_dir} is not a directory.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    for filename in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, filename)
        if os.path.isfile(src_file_path):
            file_ext = os.path.splitext(filename)[1].lower()

            # Create the subdirectory for the file extension if it doesn't exist
            dest_subdir = os.path.join(dest_dir, file_ext[1:])
            if not os.path.isdir(dest_subdir):
                os.mkdir(dest_subdir)

            dest_file_path = os.path.join(dest_subdir, filename)
            shutil.move(src_file_path, dest_file_path)


def main(args):
    parser = argparse.ArgumentParser(description="Sorts all files in the source directory by extension and moves them to their respective subdirectories in the destination directory")
    parser.add_argument("src_dir", type=str, help="The source directory to sort")
    parser.add_argument("dest_dir", type=str, help="The destination directory to move the sorted files to")
    parsed_args = parser.parse_args(args)

    sort_files_by_extension(parsed_args.src_dir, parsed_args.dest_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
