"""
Module Name: github_watcher

Description: This module provides functions for watching Github repositories.

Author: Sudo-Ivan
"""

import os
import sys
import argparse
import json
import csv
import requests
import time
from datetime import datetime, timedelta
from threading import Thread


# Constants
GITHUB_API_URL = "https://api.github.com"
GITHUB_API_VERSION = "application/vnd.github.v3+json"
RATE_LIMIT_REMAINING_HEADER = "X-RateLimit-Remaining"
RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"


def get_repositories(token):
    """
    Get all repositories from Github API.

    Args:
        token (str): Github API token.

    Returns:
        list: A list of dictionaries, where each dictionary represents a repository.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": GITHUB_API_VERSION
    }
    url = f"{GITHUB_API_URL}/repositories"
    repositories = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repositories += response.json()
        if "Link" in response.headers:
            links = response.links
            if "next" in links:
                url = links["next"]["url"]
            else:
                url = None
        else:
            url = None
    return repositories


def filter_repositories(repositories, type=None, specific=None, user=None, org=None, names=None, tags=None, stars=None):
    """
    Filter repositories based on type, specific, user, org, names, tags and stars.

    Args:
        repositories (list): A list of dictionaries, where each dictionary represents a repository.
        type (str): Type of repository (code, optional).
        specific (str): Specific repository to watch.
        user (str): User to watch.
        org (str): Organization to watch.
        names (list): List of repository names to watch.
        tags (list): List of tags to watch.
        stars (int): Number of stars a repository should have to be watched.

    Returns:
        list: A list of filtered repositories.
    """
    filtered_repositories = []
    for repository in repositories:
        if type and repository["has_issues"] != True:
            continue
        if specific and repository["full_name"] != specific:
            continue
        if user and repository["owner"]["type"] == "User" and repository["owner"]["login"] != user:
            continue
        if org and repository["owner"]["type"] == "Organization" and repository["owner"]["login"] != org:
            continue
        if names and repository["full_name"] not in names:
            continue
        if tags and not set(tags).issubset(set(repository["topics"])):
            continue
        if stars and repository["stargazers_count"] < stars:
            continue
        filtered_repositories.append(repository)
    return filtered_repositories


def watch_repository(token, repository, log_file=None, display_active=None):
    """
    Watch a repository and log any changes.

    Args:
        token (str): Github API token.
        repository (dict): A dictionary representing a repository.
        log_file (str): Path to the log file (csv or json, optional).
        display_active (bool): Display active repositories in terminal (yes or no, optional).

    Returns:
        None
    """
    url = f"{GITHUB_API_URL}/repos/{repository['full_name']}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": GITHUB_API_VERSION
    }
    active_repository = {
        "name": repository["name"],
        "size": repository["size"],
        "stargazers_count": repository["stargazers_count"],
        "watchers_count": repository["watchers_count"],
        "forks_count": repository["forks_count"],
        "updated_at": repository["updated_at"]
    }
    print(f"Watching repository: {repository['full_name']}")
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            reset_time = datetime.fromtimestamp(int(response.headers[RATE_LIMIT_RESET_HEADER]))
            wait_time = (reset_time - datetime.now()).total_seconds() + 10
            print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            response.raise_for_status()
            data = response.json()
            if data["size"] != repository["size"] or data["stargazers_count"] != repository["stargazers_count"] or data["watchers_count"] != repository["watchers_count"] or data["forks_count"] != repository["forks_count"]:
                active_repository["size"] = data["size"]
                active_repository["stargazers_count"] = data["stargazers_count"]
                active_repository["watchers_count"] = data["watchers_count"]
                active_repository["forks_count"] = data["forks_count"]
                active_repository["updated_at"] = data["updated_at"]
                print(f"{repository['full_name']} has been updated!")
                if log_file:
                    if log_file.endswith(".csv"):
                        with open(log_file, "a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([datetime.now(), repository["full_name"], active_repository["size"], active_repository["stargazers_count"], active_repository["watchers_count"], active_repository["forks_count"], active_repository["updated_at"]])
                    elif log_file.endswith(".json"):
                        with open(log_file, "a") as file:
                            json.dump({
                                "timestamp": datetime.now().isoformat(),
                                "repository": repository["full_name"],
                                "size": active_repository["size"],
                                "stargazers_count": active_repository["stargazers_count"],
                                "watchers_count": active_repository["watchers_count"],
                                "forks_count": active_repository["forks_count"],
                                "updated_at": active_repository["updated_at"]
                            }, file)
                if display_active:
                    print(f"Active repositories:\n{active_repository}")
            repository["size"] = data["size"]
            repository["stargazers_count"] = data["stargazers_count"]
            repository["watchers_count"] = data["watchers_count"]
            repository["forks_count"] = data["forks_count"]
            repository["updated_at"] = data["updated_at"]
        time.sleep(60)

def watch_repositories(token, time_to_watch, type=None, specific=None, user=None, org=None, names=None, tags=None, stars=None, log_file=None, display_active=False):
    """
    Watch repositories based on type, specific, user, org, names, tags and stars.

    Args:
        token (str): Github API token.
        time_to_watch (timedelta): Time to watch repositories.
        type (str): Type of repository (code, optional).
        specific (str): Specific repository to watch.
        user (str): User to watch.
        org (str): Organization to watch.
        names (list): List of repository names to watch.
        tags (list): List of tags to watch.
        stars (int): Number of stars a repository should have to be watched.
        log_file (str): Path to the log file (csv or json, optional).
        display_active (bool): Display active repositories in terminal (optional).

    Returns:
        None
    """
    end_time = datetime.now() + time_to_watch
    repositories = get_repositories(token)
    filtered_repositories = filter_repositories(repositories, type, specific, user, org, names, tags, stars)
    print(f"Watching {len(repositories)} repositories...")
    threads = []
    with open(log_file, "a", newline="") as file:
        csv_writer = csv.writer(file)
        while datetime.now() < end_time:
            active_repositories = []
            for repository in filtered_repositories:
                thread = Thread(target=watch_repository, args=(token, repository, file, display_active))
                thread.start()
                threads.append(thread)
                active_repositories.append(repository["full_name"])
            if display_active:
                print(f"Active repositories: {', '.join(active_repositories)}")
            time.sleep(60)
        for thread in threads:
            thread.join()
    print("Done watching repositories.")

def main(args):
    """
    Main function to handle command-line arguments and call appropriate functions.

    Args:
        args (list): List of command-line arguments.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Watch Github repositories.")
    parser.add_argument("token", type=str, help="Github API token.")
    parser.add_argument("time_to_watch", type=int, help="Time to watch repositories (in minutes).")
    parser.add_argument("--type", type=str, help="Type of repository (code, optional).")
    parser.add_argument("--specific", type=str, help="Specific repository to watch.")
    parser.add_argument("--user", type=str, help="User to watch.")
    parser.add_argument("--org", type=str, help="Organization to watch.")
    parser.add_argument("--names", type=str, help="List of repository names to watch.")
    parser.add_argument("--tags", type=str, help="List of tags to watch.")
    parser.add_argument("--stars", type=int, help="Number of stars a repository should have to be watched.")
    parser.add_argument("--log_file", type=str, help="Path to the log file (csv or json, optional).")
    parser.add_argument("--display_active", action="store_true", help="Display active repositories in terminal (optional).")
    parsed_args = parser.parse_args(args)

    time_to_watch = timedelta(minutes=parsed_args.time_to_watch)
    names = parsed_args.names.split(",") if parsed_args.names else None
    tags = parsed_args.tags.split(",") if parsed_args.tags else None

    watch_repositories(
        parsed_args.token,
        time_to_watch,
        type=parsed_args.type,
        specific=parsed_args.specific,
        user=parsed_args.user,
        org=parsed_args.org,
        names=names,
        tags=tags,
        stars=parsed_args.stars,
        log_file=parsed_args.log_file,
        display_active=parsed_args.display_active
    )

if __name__ == "__main__":
    main(sys.argv[1:])