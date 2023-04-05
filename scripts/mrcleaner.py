import os
import sys
import argparse
import concurrent.futures


def clean_directory(dir_path, file_ext, num_workers, remove_empty=False):
    count_files = 0
    count_dirs = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if not f.endswith(file_ext):
                    future = executor.submit(os.remove, os.path.join(root, f))
                    futures.append(future)
                    count_files += 1
            if remove_empty and not os.listdir(root):
                future = executor.submit(os.rmdir, root)
                futures.append(future)
                count_dirs += 1
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except OSError as e:
                print(f"Error deleting file/directory: {e}")
        print(f"Total {count_files} files deleted.")
        if remove_empty:
            print(f"Total {count_dirs} empty directories deleted.")


def empty_folder_remover(dir_path, num_workers):
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for dir in dirs:
                future = executor.submit(os.rmdir, os.path.join(root, dir))
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                count += 1
            except OSError as e:
                print(f"Error deleting directory: {e}")
        print(f"Total {count} empty directories deleted.")


def main(args):
    parser = argparse.ArgumentParser(description="Clean directory by removing all files except files with specified extension")
    parser.add_argument("dir_path", type=str, help="The directory path to clean")
    parser.add_argument("--file-ext", type=str, default=".py", help="The file extension to keep (default: .py)")
    parser.add_argument("--num-workers", type=int, default=5, help="The number of worker threads to use (default: 5)")
    parser.add_argument("--remove-empty", action="store_true", help="Remove empty directories")
    parsed_args = parser.parse_args(args)

    if not os.path.isdir(parsed_args.dir_path):
        print(f"Error: {parsed_args.dir_path} is not a directory.")
        return
    else:
        print(f"Cleaning directory: {parsed_args.dir_path}")
        clean_directory(parsed_args.dir_path, parsed_args.file_ext, parsed_args.num_workers, parsed_args.remove_empty)
        if parsed_args.remove_empty:
            empty_folder_remover(parsed_args.dir_path, parsed_args.num_workers)


if __name__ == "__main__":
    main(sys.argv[1:])
