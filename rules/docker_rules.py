'''This module will contain compliance rules
for Dockerfiles and docker-compose files.'''

import re

from rules.base_rule import BaseRule

class DockerLatestTagRule(BaseRule):
    '''check if dockerfile uses latest tag which is unpredicateble'''
    def __init__(self):
        super().__init__(
            rule_id = "DOCKER_001",
            rule_name="Avoid 'latest' tag in FROM instruction",
            category = "Docker"
        )
    
    def check(self,files):
        results = []
        #if no docker files, nothing to check
        if not files.get("dockerfiles"):
            return results
        
        for dockerfile in files["dockerfiles"]:
            content = dockerfile["content"]
            path = dockerfile["path"]

            #find all FROM instructions
            from_lines = re.findall(r"^FROM\s+.+", content, re.MULTILINE)

            for line in from_lines:
                #check if the line contains ':latest' or has no tag
                if ":latest" in line:
                    results.append(self.make_result(
                        status="FAIL",
                        message=f"[{path}] Uses 'latest' tag: {line.strip()}" 
                    ))
                elif ":" not in line.split()[-1] and "@" not in line:
                    #if no tag specified, default to latest
                    results.append(self.make_result(
                        status="FAIL",
                        message=f"[{path}] No tag specified (defaults to latest): {line.strip()}"
                    ))
        
        #if no violations, add a PASS result
        if not results:
            results.append(self.make_result(
                status="PASS",
                message="All FROM instructions are pinned versions"
            ))
        return results

class DockerRootUserRule(BaseRule):
    """check if dockerfile specifies a non root user"""
    def __init__(self):
        super().__init__(
            rule_id="DOCKER_002",
            rule_name="use non-root USER in Dockerfile",
            category="Docker"
    )
        
    def check(self,files):
        results = []

        if not files.get("dockerfiles"):
            return results
        for dockerfile in files["dockerfiles"]:
            content = dockerfile["content"]
            path = dockerfile["path"]

            #check if user instruction exists (case insensitive)
            user_match = re.search(r"(?i)^USER\s+\S+", content, re.MULTILINE)

            if user_match:
                user_line = user_match.group().strip()
                #check if its not setting user to root
                if re.search(r"(?i)^USER\s+(root|0)\s*$", user_line):
                    results.append(self.make_result(
                        status="FAIL",
                        message=f"[{path}] User is set to root: {user_line}"
                    ))
                else:
                    results.append(self.make_result(
                        status="PASS",
                        message=f"[{path}] Non_root user specified: {user_line}"
                    ))
            else:
                results.append(self.make_result(
                    status="FAIL",
                    message=f"[{path}] No USER instruction found - container runs as root"
                ))
        return results

class DockerSensitivePortRule(BaseRule):
    """check if dockerfile exposes sensitive ports"""
    #sensitive ports
    SENSITIVE_PORTS = {
        "22": "SSH",
        "23": "Telnet",
        "3306": "MySQL",
        "5432": "PostgreSQL",
        "6379": "Redis",
        "27017": "MongoDB",
    }

    def __init__(self):
        super().__init__(
            rule_id="DOCKER_003",
            rule_name="Avoid exposing sensitive ports",
            category="Docker"
        )
        

    def check(self,files):
        results = []

        if not files.get("dockerfiles"):
            return results
        
        for dockerfile in files["dockerfiles"]:
            content = dockerfile["content"]
            path = dockerfile["path"]

            expose_lines = re.findall(r"(?i)^EXPOSE\s+.+", content, re.MULTILINE)

            found_sensitive = False
            for line in expose_lines:
                #extract port nos
                ports = re.findall(r"\b(\d+)\b", line)

                for port in ports:
                    if port in self.SENSITIVE_PORTS:
                        found_sensitive = True
                        service = self.SENSITIVE_PORTS[port]
                        results.append(self.make_result(
                            status="FAIL",
                            message=f"[{path}] exposes sensitive port {port} ({service})"
                        ))
            if not found_sensitive and expose_lines:
                results.append(self.make_result(
                    status="PASS",
                    message=f"[{path}] no sensitive ports exposed"
                ))
        return results
    
    def get_docker_rules():
        """return a list of all docker rule instances"""
        return [
            DockerLatestTagRule(),
            DockerRootUserRule(),
            DockerSensitivePortRule(),
        ]
                                      


        
