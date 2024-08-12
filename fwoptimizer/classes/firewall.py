"""_summary_
"""

from fwoptimizer.classes.fdd import FDD, FieldList
from fwoptimizer.classes.rules import RuleSet


class Firewall:
    """_summary_
    """
    
    def __init__(self, fieldList: FieldList = None, fdds: list[FDD] = [], inputRules: RuleSet= None):
        """
        Firewall Constructor

        Args:
            fieldList (FieldList, optional): Firewall's Field List. Defaults to None.
            fdds (list[FDD], optional): Firewall's list of FDDs. Defaults to [].
            inputRules (RuleSet, optional): Firewall's initial rules. Defaults to None.
        """
        self.fddList: list[FDD]  = fdds
        self.fieldList: FieldList = fieldList
        self.inputRules: RuleSet = inputRules
        self.outputRules: RuleSet = None
    
    def addFdd(self, fdd: FDD):
        """
        Add FDD to the Firewall

        Args:
            fdd (FDD): FDD to add
        """
        if not isinstance(fdd, FDD):
            raise ValueError("Object is not of type FDD.")
        
        self.fddList.append(fdd)
    
    def delFDD(self, fdd: FDD):
        """
        Remove FDD from the firewall

        Args:
            fdd (FDD): FDD to remove
        """
        
