"""_summary_
"""

import os

import model.fwoManager as fwm
import views.fwoView as fwv
import views.customWidgets as cw

class ConsoleCommands:
    """
    Console Emulator for the user interaction with the model.
    """
    def __init__(self, model: fwm.FWOManager, view: fwv.FWOView, console: cw.ConsoleWidget):
        self.model = model
        self.view = view
        self.console = console
        # Permited Commands
        self.commands = {
            "import": self.importRules,
            "display": self.displayRules,
            "addfields": self.addFieldList,
            "generate": self.generateFdds,
            "optimize": self.optimizeFdds,
            "export": self.exportRules,
            "print": self.printFdd,
            "filter": self.filterFdd
        }

    def executeCommand(self, commandLine):
        """
        Execute some of the permited commands.

        Args:
            commandLine (str): Command input
        """
        try:
            # Split the command from the rest
            parts = commandLine.split(maxsplit=1) 
            command = parts[0].lower()
            arguments = parts[1] if len(parts) > 1 else ""

            if command in self.commands:
                self.commands[command](arguments)
            elif command == "help":
                self.console.appendToConsole("Available commands are: " + ", ".join(self.commands.keys()))
            elif command == "clear":
                self.console.clear()
            else:
                self.console.appendToConsole("Invalid command, type 'help' for more information.")
        except (ValueError,IndexError):
            self.console.appendToConsole("Invalid command, type 'help' for more information.")
            return

    def importRules(self, args):
        """
        Import rules from a file. Warn the user if rules already exist.

        Args:
            args (str): Command arguments, should contain the file path.
        """
        filePath = args.strip()

        if not filePath:
            self.console.appendToConsole("No file path provided. Use: import <path>")
            return
        
        if self.model.currentFirewall is None:
            self.console.appendToConsole("No firewall instantiated")

        if self.model.currentFirewall.getInputRules():
            self.console.appendToConsole("Warning: The current firewall already has input rules. Importing new rules will overwrite them.")
            
        if not os.path.exists(filePath):
            self.console.appendToConsole(f"No such file or directory: {filePath}")
            return

        fileContent, rules = self.model.importRules(filePath)
        
        if fileContent and rules:
            self.view.displayImportedRules(fileContent, rules)
            self.console.appendToConsole(f"Rules imported from {filePath}.")
        else:
            self.console.appendToConsole(f"Failed to import rules from {filePath}. Please check the file path and format.")

    def displayRules(self, args):
        """
        Display rules in the console. The user can filter by table and chain.

        Args:
            args (str): Command arguments, can specify table and chain.
        """
        parts = args.split()
        rules = self.model.currentFirewall.getInputRules()
        
        if rules is None:
            self.console.appendToConsole("No rules available.")
            return

        # If no table or chain is specified, display all rules
        if len(parts) == 0:
            self.console.appendToConsole("Displaying all rules:\n")
            self.console.appendToConsole(str(rules))
            return

        # If table is specified
        table = parts[0]
        chain = parts[1] if len(parts) > 1 else None

        if chain:
            disRules = rules[table][chain]
            if disRules:
                self.console.appendToConsole(f"Displaying rules for table '{table}' and chain '{chain}':\n")
                self.console.appendToConsole(str(disRules))
            else:
                self.console.appendToConsole(f"No rules found for table '{table}' and chain '{chain}'.")
        else:
            disRules = rules[table]
            if disRules:
                self.console.appendToConsole(f"Displaying rules for table '{table}':\n")
                self.console.appendToConsole(str(disRules))
            else:
                self.console.appendToConsole(f"No rules found for table '{table}'.")
    
    def addFieldList(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        self.console.appendToConsole("TODO")
        pass
    
    def generateFdds(self, args):
        """
        Generate FDDs for a specific table and chain, or prompt the user to choose.

        Args:
            args (str): Command arguments, can specify table and chain.
        """
        parts = args.split(',')

        # Ensure a field list is loaded
        if self.model.currentFirewall.getFieldList() is None:
            self.console.appendToConsole("No Field List loaded.\nPlease import it first.")
            return

        # Ensure rules are loaded
        if not self.model.currentFirewall or not self.model.currentFirewall.getInputRules():
            self.console.appendToConsole("No rules loaded.\nPlease import rules first.")
            return

        # Get all tables
        tables = self.model.currentFirewall.getInputRules().getTables()

        # If table and chain are specified, generate FDD for that specific table/chain
        if len(parts) == 2:
            tableName = parts[0]
            chainName = parts[1]
            if tableName in tables and chainName in tables[tableName].getChains().keys():
                self.model.generateFDD(tableName, chainName)
                self.console.appendToConsole(f"FDD generated for table '{tableName}' and chain '{chainName}'.")
            else:
                self.console.appendToConsole(f"Invalid table '{tableName}' or chain '{chainName}' specified.")
            return
        elif len(parts) == 1:
            self.console.appendToConsole(f"Invalid syntax. Use: generate &lt;table&gt;,&lt;chain&gt")
            return

        # Else, generate all
        self.model.generateFDD()
        self.console.appendToConsole("FDDs generated for all tables and chains.")
        return
    
    def optimizeFdds(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        fdds = self.model.currentFirewall.getFDDs()
        
        if not self.model.currentFirewall or len(fdds) == 0:
            self.console.appendToConsole("No FDDs generated yet. Please generate FDDs first.")
            return

        # Split arguments by comma and handle optional parameters
        try:
            table, chain = args.split(',')
        except ValueError:
            self.console.appendToConsole(f"Invalid syntax. Use: optimize &lt;table&gt;,&lt;chain&gt")
            return

        if self.model.currentFirewall.getFDD(table, chain):
            self.model.optimizeFDD(table, chain)
            self.console.appendToConsole(f"FDD for {table}/{chain} optimized.")
        else:
            self.console.appendToConsole(f"FDD for {table}/{chain} not found.")
    
    def exportRules(self, args):
        """
        Generate Rules from an specific FDD and export them to a file

        Args:
            args (str): parameters
        """
        fdds = self.model.currentFirewall.getFDDs()
        
        if not self.model.currentFirewall or len(fdds) == 0:
            self.console.appendToConsole("No FDDs generated yet. Please generate FDDs first.")
            return

        # Split arguments by comma and handle optional parameters
        try:
            table_chain, filePath = args.split()
            tableName, chainName = table_chain.split(',')
        except ValueError:
            self.console.appendToConsole(f"Invalid syntax. Use: export &lt;table&gt;,&lt;chain&gt; &lt;fileName&gt")
            return

        if self.model.currentFirewall.getFDD(tableName, chainName): 
            # Generate Rules
            exportedRules, _ = self.model.exportRules(filePath, tableName, chainName)
            self.console.appendToConsole(f"FDD for {tableName}/{chainName} optimized.")
            
            # Generate export File from RuleSet, given the Parser Strategy
            fileContent = self.model.getParserStrategy().compose(exportedRules)
            
            # Save exported rules to right menu 
            if fileContent:
                self.view.displayExportedRules(fileContent)
                
                # Write the file content to the specified file path
                with open(filePath, 'w') as file:
                    file.write(fileContent)
                
                self.console.appendToConsole(f'Exported file to: {filePath}')
        else:
            self.console.appendToConsole(f"FDD for {tableName}/{chainName} not found.")
    
    def printFdd(self, args):
        """
        Display the FDD using the console

        Args:
            arguments (str): parameters
        """
        fdds = self.model.currentFirewall.getFDDs()
        
        if not self.model.currentFirewall or len(fdds) == 0:
            self.console.appendToConsole("No FDDs generated yet. Please generate FDDs first.")
            return

        # Split arguments by comma and handle optional parameters
        try:
            table_chain, *optional_args = args.split()
            table, chain = table_chain.split(',')
        except ValueError:
            self.console.appendToConsole(f"Invalid syntax. Use: print &lt;table&gt;,&lt;chain&gt; [output_format] [graph_dir] [unroll_decisions]")
            return
        
        # Define valid options
        valid_options = {
            "outputFrmt": {'svg', 'png', 'jpg'},
            "graphDir": {'TB', 'BT', 'LR', 'RL'},
            "unroll": {'True', 'False'}
        }

        if self.model.currentFirewall.getFDD(table, chain): 
            # Handle optional parameters
            outputFrmt      = optional_args[0] if len(optional_args) > 0 else 'svg'
            graphDir        = optional_args[1] if len(optional_args) > 1 else 'TB'
            unroll          = optional_args[2] if len(optional_args) > 2 else 'False'
           
            # Validate optional parameters
            if outputFrmt not in valid_options["outputFrmt"]:
                self.console.appendToConsole(f"Invalid output format: {outputFrmt}. Choose from {valid_options['outputFrmt']}")
                return
            if graphDir not in valid_options["graphDir"]:
                self.console.appendToConsole(f"Invalid graph direction: {graphDir}. Choose from {valid_options['graphDir']}")
                return
            if unroll not in valid_options["unroll"]:
                self.console.appendToConsole(f"Invalid unroll option: {unroll}. Choose 'True' or 'False'")
                return
            
            # Convert unroll to a boolean
            unroll = unroll == 'True'
            
            pathName, imgFormat= self.model.viewFDD(table, chain, outputFrmt, graphDir, unroll)
            if self.model.graphicsView:
                self.model.graphicsView.displayImage(f'{pathName}.{imgFormat}')
            else:
                self.view.displayErrorMessage("Image Display not set.")
            self.console.appendToConsole(f"FDD for {table}/{chain} printed.")
        else:
            self.console.appendToConsole(f"FDD for {table}/{chain} not found.")
            
    def filterFdd(self, args):
        """
        Filter a FDD using the console
        
        Args:
            arguments (str): parameters
        """
        fdds = self.model.currentFirewall.getFDDs()
        
        if not self.model.currentFirewall or len(fdds) == 0:
            self.console.appendToConsole("No FDDs generated yet. Please generate FDDs first.")
            return

        # Split arguments by comma and handle optional parameters
        try:
            parts = args.split()
            table_chain, field, matchExpr = parts[0], parts[1], parts[2]
            table, chain = table_chain.split(',')
        except (ValueError,IndexError):
            self.console.appendToConsole(f"Invalid syntax. Use: filter &lt;table&gt;,&lt;chain&gt; &lt;field&gt; &lt;MatchExpression&gt;")
            return
        
        fields = [f.getName() for f in self.model.currentFirewall.getFieldList().getFields()]
        if field not in fields:
            self.console.appendToConsole(f"Invalid Field. This firewall uses:\n{fields}")
            return

        if self.model.currentFirewall.getFDD(table, chain): 
            #Filter the FDD Graph
            pathName, imgFormat= self.model.filterFDD(table, chain, field, matchExpr)
            if not pathName:
                self.console.appendToConsole("No results for filter.")
                return
            if self.model.graphicsView:
                self.model.graphicsView.displayImage(f'{pathName}.{imgFormat}')
            else:
                self.view.displayErrorMessage("Image Display not set.")
            self.console.appendToConsole(f"Filtered FDD for {table}/{chain} printed.")
        else:
            self.console.appendToConsole(f"FDD for {table}/{chain} not found.")
