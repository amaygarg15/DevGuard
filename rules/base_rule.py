# This module will define the base class that
# all compliance rules must inherit from.

from abc import ABC, abstractmethod

class BaseRule(ABC):
    #abstract base class that all compliance rules must inherit from
    def __init__(self, rule_id, rule_name, category):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.category = category

    @abstractmethod
    def check(self,files):
        '''compliance check by child class
        Args:
            files: dictionary of devops from file_loader
        returns:
            a list of result dictionaries'''
        pass

    def make_result(self, status, message):
        '''standard result dictionary'''
        return{
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category,
            "status": status,
            "message": message,
        }
    
def run_rules(rule_list, files):
    '''run a list of rule instances for scanned files'''
    all_results =[]

    for rule in rule_list:
        results = rule.check(files)
        all_results.extend(results)
    return all_results