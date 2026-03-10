# repo_scanner.py
# Phase 3: This module will handle cloning a GitHub repo
# or validating a local repository path.

import os
import tempfile

from git import Repo, GitCommandError

#validate that a local path exists and is a directory 
def scan_local_repo(path):
    absolute_path = os.path.abspath(path)

    if not os.path.exists(absolute_path):
        print(f"Error: Path '{absolute_path}' does not exist")
        return None
    
    if not os.path.exists(absolute_path):
        print(f"Error: Path '{absolute_path}' is not a directory")
        return None
    
    print(f"Local repository found: {absolute_path}")
    return absolute_path

#Clone a GitHub repo to a temporary directory
def clone_remote_repo(url):
    temp_dir = tempfile.mkdtemp(prefix="devguard_")
    print(f"Cloning repository: {url}")
    print(f"Temporary diretory: {temp_dir}")

    try:
        Repo.clone_from(url, temp_dir)
        print("Clone successful.")
        return temp_dir
    except GitCommandError as e:
        print(f"Error: Failed to clone repository.\n{e}")
        return None
    
def get_repo_path(path=None, url=None):
    if path:
        return scan_local_repo(path)
    elif url:
        return clone_remote_repo(url)
    else:
        print("Error: No path or URL provided")
        return None

                          

