# file_loader.py
# Phase 3: This module will walk through the repository
# and find DevOps config files (Dockerfiles, CI pipelines, etc).

import os 
# File patterns we look for when scanning a repository.
# Each key is a category, and the value describes how to match files.
DEVOPS_PATTERNS = {
    "dockerfiles": {
        "filenames": ["Dockerfile"],
        "description": "Docker container definations"
    },
    "compose_files": {
        "filenames": ["docker-compose.yml", "docker-compose.yml"],
        "description": "Docker Compose multi-container configs"
    },
    "ci_workflows": {
        "directory": ".github/workflows",
        "extensions": [".yml", ".yaml"],
        "description": "GitHub Actions CI/CD pipelines"
    },
    "kubernetes_files": {
        "directory": "k8s",
        "extensions": [".yml", ".yaml"],
        "description": "Kubernetes manifest files"
    },
}

def load_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None
    
def find_devops_files(repo_path):
    results = {
        "dockerfiles": [],
        "compose_files": [],
        "ci_workflows": [],
        "kubernetes_files": [],
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d for d in dirs
            if d == ".github" or not d.startswith(".")
        ]

        relative_root = os.path.relpath(root, repo_path)

        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.join(relative_root, filename)

            relative_path = relative_path.replace("\\", "/")

            if relative_path.startswith("./"):
                relative_path = relative_path[2:]

            #check if dockerfiles?
            if filename in DEVOPS_PATTERNS["dockerfiles"]["filenames"]:
                content = load_file_content(full_path)
                if content:
                    results["dockerfiles"].append({
                        "path": relative_path,
                        "content": content
                    })
            #check if dockerfile compose?
            elif filename in DEVOPS_PATTERNS["compose_files"]["filenames"]:
                content = load_file_content(full_path)
                if content:
                    results["compose_files"].append({                            "path": relative_path,
                           "content": content
                    })
            #check in github actions workflow?
            elif (DEVOPS_PATTERNS["ci_workflows"]["directory"]) in relative_path.replace("\\", "/"):
                _, ext = os.path.splitext(filename)
                if ext in DEVOPS_PATTERNS["ci_workflows"]["extensions"]:
                    content = load_file_content(full_path)
                    if content:
                        results["ci_workflows"].append({
                            "path": relative_path,
                            "content": content
                        })
            #check if kubernetes manifest?
            elif (DEVOPS_PATTERNS["kubernetes_files"]["directory"]) in relative_path.replace("\\", "/"):
                _, ext = os.path.splitext(filename)
                if ext in DEVOPS_PATTERNS["kubernetes_files"]["extensions"]:
                    content = load_file_content(full_path)
                    if content:
                        results["kubernetes_files"].append({
                            "path": relative_path,
                            "content": content
                        })
    return results

def print_scan_summary(files):
    print("\nScan Results:")
    print("-" * 40)

    total = 0
    for category, items in files.items():
        count = len(items)
        total += count
        label = DEVOPS_PATTERNS[category]["description"]
        if count > 0:
            print(f" Found {count} {label}:")
            for item in items:
                print(f" -{item['path']}")
        else:
            print(f" No {label} found.")
    
    print("-" * 40)
    print(f" Total DevOps files found: {total}\n")

    return total
            
            