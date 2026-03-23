import argparse
import sys
import json

from scanner.repo_scanner import get_repo_path
from scanner.file_loader import find_devops_files, print_scan_summary
from rules.base_rule import run_rules
from rules.docker_rules import get_docker_rules
from rules.cicd_rules import get_cicd_rules
from rules.security_rules import get_security_rules
from reports.report_generator import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="DevGuard - DevOps Compliance Checker"
    )

    parser.add_argument(
        "--path",
        type=str,
        help="Local path to the repository to scan"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="GitHub repository URL to clone and scan"
    )

    args = parser.parse_args()

    if not args.path and not args.url:
        parser.print_help()
        print("\nError: Provide either --path or --url to scan a repository.")
        sys.exit(1)

    print("=" * 50)
    print("   DEVGUARD - DevOps Compliance Checker")
    print("=" * 50)

    #get repo path
    repo_path = get_repo_path(path = args.path, url=args.url)
    if not repo_path:
        print("Aborting: Could not access the repository")
        sys.exit(1)

    #find devops comfig files
    files = find_devops_files(repo_path)
    total_files = print_scan_summary(files)

    if total_files == 0:
        print("NO DevOps configuration files found, Nothing to check.")
        sys.exit(0)
    
    print("Running compliance checks")

    #gather all rules
    rules_to_run = []
    rules_to_run.extend(get_docker_rules())
    rules_to_run.extend(get_cicd_rules())
    rules_to_run.extend(get_security_rules())


    #run
    all_results = run_rules(rules_to_run, files)

    #print results
    all_passed = generate_report(all_results)

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
