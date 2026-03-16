# This module will contain compliance rules
# for CI/CD pipeline files (GitHub Actions workflows).

import yaml
from rules.base_rule import BaseRule

class PipelineExistsRule(BaseRule):
    """check if any ci/cd pipeline config exists"""
    def __init__(self):
        super().__init__(
            rule_id="CICD_001",
            rule_name="Ensure CI/CD pipeline exists",
            category="CI/CD"
        )

    def check(self, files):
        results = []
        workflows = files.get("ci_workflows", [])

        if not workflows:
            results.append(self.make_result(
                status="FAIL",
                message="NO GitHub Actions workflows found"
            ))
        else:
            results.append(self.make_result(
                status="PASS",
                message=f"Found {len(workflows)} CI/CD workflow(s)"
            ))
        return results
    
class TestStageExistsRule(BaseRule):
    """check if pipleline contains a step or job related to testing"""
    def __init__(self):
        super().__init__(
            rule_id="CICD_002",
            rule_name="Ensure pipeline contains a test stage",
            category="CI/CD"
        )
    def check(self, files):
        results =[]
        workflows = files.get("ci_workflows", [])

        if not workflows:
            return results
        
        for workflow in workflows:
            content = workflow.get("content", "")
            path = workflow.get("path", "Unknown")

            try:
                # yaml.safe_load converts the YAML string into a Python dictionary
                parsed_yaml = yaml.safe_load(content)
                if not isinstance (parsed_yaml, dict):
                    continue

                jobs = parsed_yaml.get("jobs", {})
                has_test = False

                for job_name, job_data in jobs.items():
                    if "test" in job_name.lower():
                        has_test = True
                        break

                    if isinstance(job_data, dict):
                        steps = job_data.get("steps", [])
                        for step in steps:
                            if "run" in step and "test" in str(step.get("run", "")).lower():
                                has_test = True
                                break
                            if "name" in step and "test" in str(step.get("name", "")).lower():
                                has_test = True
                                break
                if has_test:
                    results.append(self.make_result(
                        status="PASS",
                        message=f"[{path}] Pipeline includes testing stages."
                    ))
                else:
                    results.append(self.make_result(
                    status="FAIL",
                    message=f"[{path}] No test stage or test commands found."
                ))
            
            except yaml.YAMLError as e:
                results.append(self.make_result(
                    status="FAIL",
                    message=f"[{path}] Invalid YAML format: {e}"
                ))
                    
        return results
    
class SecureActionsVersionRule(BaseRule):
    """check if GitHub Actions avoid using @master or @latest tags"""
    def __init__(self):
        super().__init__(
            rule_id="CICD_003",
            rule_name="Pin GitHub Actions to specific versions",
            category="CI/CD"
        )

    def check(self, files):
        results = []
        workflows = files.get("ci_workflows", [])

        if not workflows:
            return results
        
        for workflow in workflows:
            content = workflow.get("content", "")
            path = workflow.get("path", "Unknown")

            try:
                parsed_yaml = yaml.safe_load(content)
                if not isinstance(parsed_yaml, dict):
                    continue

                jobs = parsed_yaml.get("jobs", {})
                issues_found = False

                for job_name, job_data in jobs.items():
                    if isinstance(job_data, dict):
                        steps = job_data.get("steps", [])
                        for step in steps:
                            # 'uses' dictates which standard Action is being called
                            action_used = step.get("uses", "")
                            if action_used:
                                if"@master" in action_used or "@latest" in action_used:
                                    issues_found = True
                                    results.append(self.make_result(
                                        status="FAIL",
                                        message=f"[{path}] Step uses unpinned action version: {action_used}"
                                    ))
                if not issues_found:
                    results.append(self.make_result(
                        status="PASS",
                        message=f"[{path}] All GitHub actions are pinned to secure versions."
                    ))
            except yaml.YAMLError:
                pass 
        return results

def get_cicd_rules():
    return [
        PipelineExistsRule(),
        TestStageExistsRule(),
        SecureActionsVersionRule(),
    ]

