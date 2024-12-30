"""_summary_
"""

from fwoptimizer.core.fdd import FDD, FieldList
from fwoptimizer.core.rules import RuleSet, Table
import logging, os



class Firewall:
    """_summary_
    """
    
    def __init__(self, fieldList: FieldList = None, fdds: dict[str, list[FDD]] = [], inputRules: RuleSet= None, defaultWorkFolder: str = "", logger = None):
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
        self._optRules: RuleSet = inputRules
        self._workFolder: str = defaultWorkFolder
        self._inputFile : str = None
        self._logger = logger or logging.getLogger('Firewall')
        
        # Ensure work folder exists
        if self._workFolder and not os.path.exists(self._workFolder):
            os.makedirs(self._workFolder)
            self._logger.info(f"Created work folder for Firewall at {self._workFolder}")
            
        self._logger.info("Initialized Firewall")
    
    def getWorkFolder(self):
        """
        Get current work Folder

        Returns:
            str: Work Folder
        """
        return self._workFolder
    
    def setInputFile(self, path):
        """
        Set input File path

        Args:
            path (str): Path of Input File
        """
        self._inputFile = path
        
    def getInputFile(self):
        """
        Get Input File path

        Returns:
            str: Path of Input File
        """
        return self._inputFile
      
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
    
    def setOptRules(self, rules: RuleSet):
        """
        Set Firewall Output Rules

        Args:
            rules (RuleSet): New RuleSet
        """
        if not isinstance(rules, RuleSet):
            raise ValueError("Object is not of type RuleSet.")
        
        self._optRules = rules
        
    def getOptRules(self):
        """
        Get Output Rules

        Returns:
            RuleSet: New RuleSet
        """
        return self._optRules
    
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
    
    def loadIPSets(self, ipSetFiles):
        """
        Load an IP set from a file.

        Args:
            ipSetFiles (dict): Dict of IPSet Names to file paths.
        """
        # Load IP sets into a dictionary
        self._logger.info(f"Previous Rules\n{self._inputRules}")
        ipSets = {}
        for ipSetName, filePath in ipSetFiles.items():
            self._logger.info(f"Loading IP set '{ipSetName}' from file: {filePath}")
            with open(filePath, 'r') as file:
                ipList = [
                    ip.strip() for ip in file.readlines() 
                    if ip.strip() and not ip.startswith('#')
                ]
            #TODO Copiar archivos al wd para cuando se guarde y cargue el proyecto.
            ipSets[ipSetName] = ipList
            self._logger.info(f"Loaded IPSet '{ipSetName}' with IPs: {ipList}")

        # Replace IPSet names in predicates with their corresponding IP lists
        for _, table in self._inputRules.getTables().items():
            for _, chain in table.getChains().items():
                for rule in chain.getRules():
                    updatedPredicates = {}
                    for field in ['SrcIP', 'DstIP']:
                        
                        # Get Option
                        option = rule.getOption(field, None) 
                        if option is None:
                            continue
                        
                        # Handle the case where option is a list
                        if isinstance(option, list) and len(option) == 1:
                            value = option[0]
                        elif isinstance(option, str):
                            value = option
                        else:
                            value = None
                        
                        #TODO En caso de IpSet vacio usar dominio?
                        if value in ipSets:
                            # Replace the IPSet name with its IP list
                            updatedPredicates[field] = ipSets[value]
                            self._logger.info(f"Replaced IPSet '{value}' in rule {rule.getId()} with {ipSets[value]}")
                        else:
                            # Retain the original value if it's not an IPSet name
                            updatedPredicates[field] = [value]
                    
                    # Update the rule's predicates
                    for fieldName, newValue in updatedPredicates.items():
                        rule.setPredicate(fieldName, newValue)

        #Update self._optRules to match _inputRules
        self._logger.info(f"Updated Rules\n{self._inputRules}")
        self._optRules = self._inputRules

    
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
                    self._logger.info(f'Generating {tableName} - {chainName} FDD')
                    fdd.genFDD(self._inputRules[tableName][chainName], self._workFolder + f"report-{tableName}-{chainName}.txt")
                    self._logger.info(f'{tableName} - {chainName} FDD Done.')
        else:   # Generate Specific FDD
            self._logger.info(f'Generating {table} - {chain} FDD')
            fdd = FDD(self._fieldList)
            self.addFdd(table, fdd)
            fdd.genFDD(self._inputRules[table][chain], self._workFolder + f"report-{table}-{chain}.txt")
            self._logger.info(f'{table} - {chain} FDD Done.')
                
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
            for tableName ,table in self._inputRules.getTables().items():
                for chainName, _ in table.getChains().items():
                    
                    fdd = self.getFDD(tableName, chainName)
                    if fdd is None:
                        self._logger.warning(f'No FDD generated for {tableName} - {chainName} (Skipping.)')
                        continue
                    
                    self._logger.info(f'Optimizing {tableName} - {chainName} FDD')
                    fdd.reduction()
                    fdd.marking()
                    self._logger.info(f'{tableName} - {chainName} optimization Done.')
                    
        else:   # Optimize Specific FDD
            self._logger.info(f'Optimizing {table} - {chain} FDD')
            
            fdd = self.getFDD(table, chain)
            fdd.reduction()
            fdd.marking()
            
            self._logger.info(f'{table} - {chain} optimization Done.')
    
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
                        outputChain.setDefaultDecision(outputChain[-1].getDecision()) # Set Default Chain Decision as Last Rule Decision
                        # Add new chain
                        exportRuleSet[tableName].addChain(outputChain)
                        self._logger.info(f'Exporting {tableName} - {chainName} Rules')
                    else:
                        self._logger.warning(f'FDD not found for chain: {chain} in table: {table}')
        else:  
            self._logger.info(f'Exporting {table} - {chain} Rules')
            # Add new table
            exportRuleSet.addTable(Table(table))
            # Get specific FDD
            fdd = self.getFDD(table, chain)
            if fdd:
                # Generate new chain
                outputChain = fdd.firewallGen()
                outputChain.setDefaultDecision(outputChain[-1].getDecision()) # Set Default Chain Decision as Last Rule Decision
                # Add new chain
                exportRuleSet[table].addChain(outputChain)
            else:
                self._logger.warning(f'FDD not found for chain: {chain} in table: {table}')
                        
        self._logger.info(f'Generated RuleSet:\n{exportRuleSet}')
        self.setOptRules(exportRuleSet)
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
                self._logger.warning(f"FDD not found in table {tableName}.")
        else:
            self._logger.warning(f"Table {tableName} does not exist.")

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
            self._logger.warning(f"FDD not found for chain: {chainName} in table: {tableName}")
        else:
            self._logger.warning(f"Table {tableName} not found.")
        return None
    
    def getDecisions(self):
        """
        Get all possible decisions from all FDDs in the firewall.

        Returns:
            set: A set of unique decisions from all FDDs.
        """
        all_decisions = set()  # Using a set to avoid duplicates
        for fdds in self._fddList.values():  # Iterate through all FDD lists in the firewall
            for fdd in fdds:  # Iterate through each FDD
                decisions = fdd.getDecisions()  # Get the decisions from the FDD
                all_decisions.update(decisions.keys())  # Update the set with new decisions
        return all_decisions  # Return the set of unique decisions
    
    def getFDDs(self):
        """
        Get all FDDs in the Firewall
        """
        return self._fddList
