import os
import sys
import time
import argparse
import git
import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta


def download_repo(repo_url, output_dir, csv_file):
    try:
        repo = git.Repo.clone_from(repo_url, os.path.join(output_dir, os.path.basename(repo_url)))
        print(f"Repository {repo.name} cloned.")

        # Log the repository details to CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([repo.name, repo_url, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])

    except Exception as e:
        print(f"Error cloning repository {repo_url}: {e}")


def main(args_list):
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Clone GitHub repositories based on criteria")
    parser.add_argument("--output-dir", type=str, required=True, help="The directory to save the cloned repositories")
    parser.add_argument("--stars", type=int, required=False, help="The minimum number of stars for repositories to clone")
    parser.add_argument("--size-limit", type=int, required=False, help="The maximum size limit in MB for repositories to clone")
    parser.add_argument("--code-type", type=str, required=False, help="The code type to search for on GitHub")
    parser.add_argument("--age", type=int, default=8, help="The age of repositories to search for in years")
    parser.add_argument("--csv-file", type=argparse.FileType('a'), default="cloned_repositories_log.csv", help="The name of the CSV file to log the cloned repositories")
    parser.add_argument("--by-user", type=str, required=False, help="The username of the repository owner")
    parser.add_argument("--by-organization", type=str, required=False, help="The organization name to search for repositories")
    parser.add_argument("--code-percentage", type=int, required=False, help="The percentage of code in a repository to search for")
    parser.add_argument("--repo-name", type=str, required=False, help="The repository name to search for")
    args = parser.parse_args(args_list)

    # Calculate the date range for repository search
    today = datetime.utcnow()
    oldest_date = today - timedelta(days=args.age*365)
    oldest_date_str = oldest_date.strftime('%Y-%m-%d')

    # Search for repositories and clone them in parallel
    api_url = "https://api.github.com/search/repositories"
    query = f"q=pushed:>{oldest_date_str}"
    if args.by_user:
        query += f"+user:{args.by_user}"
    if args.by_organization:
        query += f"+org:{args.by_organization}"
    if args.code_type:
        query += f"+language:{args.code_type}"
    if args.repo_name:
        query += f"+repo:{args.repo_name}"
    if args.stars:
        query += f"+stars:>={args.stars}"
    if args.size_limit:
        query += f"+size:<={args.size_limit * 1000}"
    if args.code_percentage:
        query += f"+size:<={args.code_percentage}%"

    per_page = 100
    page = 1
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    os.makedirs(args.output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        while True:
            params = f"{query}&per_page={per_page}&page={page}"
            response = requests.get(f"{api_url}?{params}", headers=headers)

        if response.status_code == 200:
            result = response.json()

            if result["total_count"] == 0:
                print("No repositories found.")

            for item in result["items"]:
                repo_url = item["clone_url"]
                repo_name = "{}".format(item["name"])
                repo_name = repo_name.replace("/", "_")
                print(f"Adding repository {repo_name} to download list...")
                futures.append(executor.submit(download_repo, repo_url, args.output_dir, args.csv_file.name))

            for future in as_completed(futures, timeout=3):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error cloning repository: {e}")

            page += 1
        else:
            print(f"Error fetching repositories: {response.status_code} - {response.reason}")

        time.sleep(3)  # Add a 3-second delay between each page request

        if not futures: # No more futures to wait for

            # Wait for futures to complete
            for future in as_completed(futures, timeout=3):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error cloning repository: {e}")

            # Remove completed futures from list
            futures = [f for f in futures if not f.done()]


if __name__ == "__main__":
    main(sys.argv[1:])

