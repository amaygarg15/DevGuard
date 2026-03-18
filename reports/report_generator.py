# This module will collect all rule results
# and generate a formatted compliance report with a score.

def print_separator(char="="):
    """Helper to print a consistent width separator."""
    print(char * 60)

def generate_report(results):
    """
    Parses the raw results from the rule engine, 
    calculates a score, and prints a formatted report.
    """
    if not results:
        print("\nNo checks were executed.")
        return

    # Count passes and fails for the score
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r["status"] == "PASS")
    failed_checks = total_checks - passed_checks

    # Group the results by their Category (Docker, CI/CD, Security)
    grouped_results = {}
    for r in results:
        category = r.get("category", "General")
        if category not in grouped_results:
            grouped_results[category] = []
        grouped_results[category].append(r)

    #HEADER
    print("\n")
    print_separator("=")
    print("   DEVGUARD COMPLIANCE REPORT".center(60))
    print_separator("=")

    #result by categories
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    for category, category_results in grouped_results.items():
        print(f"\n[{category.upper()} CHECKS]")
        print_separator("-")

        for res in category_results:
            rule_id = res.get("rule_id", "UNK")
            status = res.get("status", "FAIL")
            message = res.get("message", "")

            if status == "PASS":
                    print(f" {GREEN}✔ [PASS]{RESET} {rule_id}: {message}")
            else:
                print(f" {RED}❌ [FAIL]{RESET} {rule_id}: {message}")

    #final score
    score = (passed_checks / total_checks * 100) if total_checks > 0 else 0

    print("\n")
    print_separator("=")
    print("   EXECUTIVE SUMMARY".center(60))
    print_separator("=")
    print(f" Total Checks Run : {total_checks}")
    print(f" Passed Checks    : {passed_checks}")
    print(f" Failed Checks    : {failed_checks}")

    if score >= 90:
        score_color = GREEN
    elif score >= 60:
        score_color = '\033[93m'
    else:
        score_color = RED

    print(f"\n OVERALL COMPLIANCE SCORE: {score_color}{score:.1f}%{RESET}")
    print_separator("=")
    print("\n")

    return failed_checks == 0