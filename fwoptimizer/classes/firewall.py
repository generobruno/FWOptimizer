"""_summary_
"""

from fwoptimizer.classes.fdd import FDD, FieldList
from fwoptimizer.classes.rules import RuleSet, Table

class Firewall:
    """_summary_
    """
    
    def __init__(self, fieldList: FieldList = None, fdds: list[FDD] = [], inputRules: RuleSet= None, workFolder: str = ""):
        """
        Firewall Constructor

        Args:
            fieldList (FieldList, optional): Firewall's Field List. Defaults to None.
            fdds (list[FDD], optional): Firewall's list of FDDs. Defaults to [].
            inputRules (RuleSet, optional): Firewall's initial rules. Defaults to None.
        """
        self._fddList: list[FDD] = fdds
        self._fieldList: FieldList = fieldList
        self._inputRules: RuleSet = inputRules
        self._outputRules: RuleSet = None
        self._workFolder: str = workFolder
        
    def setInputRules(self, rules: RuleSet):
        """
        Set Firewall Input Rules

        Args:
            rules (RuleSet): Initial RuleSet
        """
        if not isinstance(rules, RuleSet):
            raise ValueError("Object is not of type RuleSet.")
        
        self._inputRules = rules
        
    def getInputRules(self):
        """
        Get Input Rules

        Returns:
            RuleSet: Initial RuleSet
        """
        return self._inputRules
    
    def setFieldList(self, filePath: str):
        """
        Set the Firewall's Field List

        Args:
            filePath (str): Firewall's Field List config file
        """
        fieldList = FieldList()
        fieldList.loadConfig(f"{filePath}")
        self._fieldList = fieldList
    
    def getFieldList(self):
        """
        Get Field List

        Returns:
            FieldList: Firewall's field list
        """
        return self._fieldList
    
    def genFdd(self, table=None, chain=None):
        """
        Generate a FDD from a specific List of Rules in the firewall's policies,
        or generate all FDDs from the firewall's policies.

        Args:
            table (Table): Table from the RuleSet
            chain (Chain): Chain in the Table
        """
        # Generate all
        if table is None and chain is None:
            for tableName , table in self._inputRules.getTables().items():
                for chainName, _ in table.getChains().items():
                    fdd = FDD(self._fieldList)
                    self.addFdd(fdd)
                    print(f'Generating {tableName} - {chainName} FDD')
                    fdd.genFDD(self._inputRules[tableName][chainName], self._workFolder + f"report-{tableName}-{chainName}.txt")
                    print(f'{tableName} - {chainName} FDD Done.')
        else:   # Generate Specific FDD
            print(f'Generating {table} - {chain} FDD')
            fdd = FDD(self._fieldList)
            self.addFdd(fdd)
            fdd.genFDD(self._inputRules[table][chain], self._workFolder + f"report-{table}-{chain}.txt")
            print(f'{table} - {chain} FDD Done.')
                
    def optimizeFdd(self, table=None, chain=None):
        """
        Optimize a FDD from a specific List of Rules in the firewall's policies,
        or optimize all FDDs from the firewall's policies.

        Args:
            table (Table): Table from the RuleSet
            chain (Chain): Chain in the Table
        """
        # Optimize all
        if table is None and chain is None:
            for tableName , table in self._inputRules.getTables().items():
                for chainName, _ in table.getChains().items():
                    fdd = self.getFDD(chainName)
                    print(f'Optimizing {tableName} - {chainName} FDD')
                    fdd.reduction()
                    fdd.marking()
                    print(f'{tableName} - {chainName} optimization Done.')
        else:   # Optimize Specific FDD
            print(f'Optimizing {table} - {chain} FDD')
            fdd = self.getFDD(chain)
            fdd.reduction()
            fdd.marking()
            print(f'{table} - {chain} optimization Done.')
    
    def genOutputRules(self, table=None, chain=None):
        """
        Generate and export output RuleSet from FDD.

        Args:
            table (str, optional): Table Name. Defaults to None.
            chain (str, optional): Chain Name. Defaults to None.

        Returns:
            RuleSet: Generated RuleSet
        """
        # Output RuleSet
        exportRuleSet = RuleSet()
        
        if table is None and chain is None:
            for tableName , table in self._inputRules.getTables().items():
                # Add new table
                exportRuleSet.addTable(Table(tableName))
                for chainName, _ in table.getChains().items():
                    fdd = self.getFDD(chainName)
                    if fdd:
                        # Generate new chain
                        outputChain = fdd.firewallGen()
                        outputChain.setDefaultDecision(outputChain[-1].getDecision()) #TODO CHECK
                        # Add new chain
                        exportRuleSet[tableName].addChain(outputChain)
                        print(f'Exporting {tableName} - {chainName} Rules')
                    else:
                        print(f'FDD not found for chain: {chain} in table: {table}')
        else:  
            print(f'Exporting {table} - {chain} Rules')
            # Add new table
            exportRuleSet.addTable(Table(table))
            # Get specific FDD
            fdd = self.getFDD(chain)
            if fdd:
                # Generate new chain
                outputChain = fdd.firewallGen()
                outputChain.setDefaultDecision(outputChain[-1].getDecision()) #TODO CHECK
                # Add new chain
                exportRuleSet[table].addChain(outputChain)
            else:
                print(f'FDD not found for chain: {chain} in table: {table}')
                        
        print(f'Generated RuleSet:\n{exportRuleSet}')
        return exportRuleSet
    
    def addFdd(self, fdd: FDD):
        """
        Add FDD to the Firewall

        Args:
            fdd (FDD): FDD to add
        """
        if not isinstance(fdd, FDD):
            raise ValueError("Object is not of type FDD.")
        
        self._fddList.append(fdd)
    
    def delFDD(self, fdd: FDD):
        """
        Remove FDD from the firewall

        Args:
            fdd (FDD): FDD to remove
        """
        removeFdd = self.getFDD(fdd)
        
        if removeFdd:
            self._fddList.remove(fdd)
        else:
            print(f"Can't remove FDD.")

    # TODO Lucho - Corregir documentación
    def getFDD(self, chainName: str):#TODO REVISAR
        """
        Get the FDD corresponding to the given table and chain.

        Args:
            table_name (str): Name of the table.
            chain_name (str): Name of the chain.

        Returns:
            FDD: The corresponding FDD if found, else None.
        """
        for fdd in self._fddList:
            if fdd.getName() == chainName:
                return fdd
        print(f"FDD not found for chain: {chainName}")
        return None
    
    def getFDDs(self):
        """
        Get all FDDs in the Firewall

        Returns:
            List[FDD]: List of FDDs 
        """
        return self._fddList
        
