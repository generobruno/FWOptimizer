"""_summary_
"""

from fwoptimizer.classes.fdd import FDD, FieldList
from fwoptimizer.classes.rules import RuleSet, Table

class Firewall:
    """_summary_
    """
    
    def __init__(self, fieldList: FieldList = None, fdds: dict[str, list[FDD]] = [], inputRules: RuleSet= None, workFolder: str = ""):
        """
        Firewall Constructor

        Args:
            fieldList (FieldList, optional): Firewall's Field List. Defaults to None.
            fdds (dict[str, list[FDD]], optional): Dictionary mapping table names to lists of FDDs. Defaults to {}.
            inputRules (RuleSet, optional): Firewall's initial rules. Defaults to None.
        """
        self._fddList: dict[str, list[FDD]] = fdds if fdds else {}
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
                    self.addFdd(tableName, fdd)
                    print(f'Generating {tableName} - {chainName} FDD')
                    fdd.genFDD(self._inputRules[tableName][chainName], self._workFolder + f"report-{tableName}-{chainName}.txt")
                    print(f'{tableName} - {chainName} FDD Done.')
        else:   # Generate Specific FDD
            print(f'Generating {table} - {chain} FDD')
            fdd = FDD(self._fieldList)
            self.addFdd(table, fdd)
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
                    fdd = self.getFDD(tableName, chainName)
                    print(f'Optimizing {tableName} - {chainName} FDD')
                    fdd.reduction()
                    fdd.marking()
                    print(f'{tableName} - {chainName} optimization Done.')
        else:   # Optimize Specific FDD
            print(f'Optimizing {table} - {chain} FDD')
            fdd = self.getFDD(table, chain)
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
                    fdd = self.getFDD(tableName, chainName)
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
            fdd = self.getFDD(table, chain)
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
    
    def addFdd(self, tableName: str, fdd: FDD):
        """
        Add FDD to the Firewall under the specified table.

        Args:
            tableName (str): Name of the table to add the FDD to.
            fdd (FDD): FDD to add.
        """
        if not isinstance(fdd, FDD):
            raise ValueError("Object is not of type FDD.")
        
        # If the table doesn't exist in the dictionary, create a new entry
        if tableName not in self._fddList:
            self._fddList[tableName] = []

        # Append the FDD to the list for the specified table
        self._fddList[tableName].append(fdd)
    
    def delFDD(self, tableName: str, fdd: FDD):
        """
        Remove FDD from the firewall under the specified table.

        Args:
            tableName (str): Name of the table to remove the FDD from.
            fdd (FDD): FDD to remove.
        """
        if tableName in self._fddList:
            # Try to find the FDD in the list for the given table
            if fdd in self._fddList[tableName]:
                self._fddList[tableName].remove(fdd)
                # If no FDDs are left in the table, remove the entry for the table
                if len(self._fddList[tableName]) == 0:
                    del self._fddList[tableName]
            else:
                print(f"FDD not found in table {tableName}.")
        else:
            print(f"Table {tableName} does not exist.")

    def getFDD(self, tableName: str, chainName: str):
        """
        Get the FDD corresponding to the given table and chain.

        Args:
            tableName (str): Name of the table.
            chainName (str): Name of the chain.

        Returns:
            FDD: The corresponding FDD if found, else None.
        """
        if tableName in self._fddList:
            # Iterate over the FDDs in the specified table
            for fdd in self._fddList[tableName]:
                if fdd.getName() == chainName:
                    return fdd
            print(f"FDD not found for chain: {chainName} in table: {tableName}")
        else:
            print(f"Table {tableName} not found.")
        return None
    
    def getFDDs(self):
        """
        Get all FDDs in the Firewall

        Returns:
            dict[str, list[str]]: Dictionary of table names and their corresponding FDD chain names.
        """
        fdd_view = {}
        for tableName, fdd_list in self._fddList.items():
            fdd_view[tableName] = [fdd.getName() for fdd in fdd_list]
        
        return fdd_view
