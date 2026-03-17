# This module will contain compliance rules
# for detecting hardcoded secrets and API keys.

import re
from rules.base_rule import BaseRule

class HardcodedSecretRule(BaseRule):
    """Detect potential hardcoded API keys, secrets, or tokens across all files."""
    def __init__(self):
        super().__init__(
            rule_id="SEC_001",
            rule_name="Avoid hardcoded secrets",
            category="Security"
        )

        # A dictionary of RegEx patterns for common secrets.
        # Note: These are simple, educational patterns. Enterprise tools use hundreds of highly specific regexes.
        self.secret_patterns = {
            # Matches generic key assignments (e.g., API_KEY=xyz, secret_token="abc")
            "Generic Secret Assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)[\s]*[:=][\s]*[\"']?([A-Za-z0-9\-_]{16,})[\"']?"),
            
            # Typical structure of an AWS Access Key ID
            "AWS Access Key": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
            
            # Common prefix for Stripe API keys
            "Stripe API Key": re.compile(r"(?i)sk_(test|live)_[0-9a-zA-Z]{24}"),
        }

    def check(self, files):
        results = []

        all_file_categories = [
            "dockerfiles",
            "compose_files",
            "ci_workflows",
            "kubernetes_files"
        ]

        for category in all_file_categories:
            file_list = files.get(category, [])
            for file_item in file_list:
                content = file_item.get("content", "")
                path = file_item.get("path", "Unknown")

                secrets_found = False

                #check line by line
                for line_number, line in enumerate(content.splitlines(), start = 1):
                    for secret_type, pattern in self.secret_patterns.items():
                        #if a pattern finds a match in the line
                        if pattern.search(line):
                            secrets_found = True
                            results.append(self.make_result(
                                status="FAIL",
                                message=f"[{path}:{line_number}] Potential {secret_type} detected. Please use environment variables or a secrets manager."
                            ))
                        
                if not secrets_found:
                    results.append(self.make_result(
                        status="PASS",
                        message=f"[{path}] No hardcoded secrets detected."
                    ))
        return results     

def get_security_rules():
    """Return a list of all security rule instances."""
    return [
        HardcodedSecretRule()
    ]  

