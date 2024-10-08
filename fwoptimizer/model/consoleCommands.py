"""_summary_
"""

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
            "print": self.printFdd
        }

    def executeCommand(self, commandLine):
        """
        Execute some of the permited commands.

        Args:
            commandLine (str): Command input
        """
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
        parts = args.split()

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
            if tableName in tables and chainName in self.model.currentFirewall.getInputRules()[tableName]:
                self.model.generateFDD(tableName, chainName)
                self.console.appendToConsole(f"FDD generated for table '{tableName}' and chain '{chainName}'.")
            else:
                self.console.appendToConsole(f"Invalid table '{tableName}' or chain '{chainName}' specified.")
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
        self.console.appendToConsole("TODO")
        pass
    
    def exportRules(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        self.console.appendToConsole("TODO")
        pass
    
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

        if self.model.currentFirewall.getFDD(chain): #TODO REVISAR
            # Handle optional parameters
            outputFrmt      = optional_args[0] if len(optional_args) > 0 else None
            graphDir        = optional_args[1] if len(optional_args) > 1 else None
            unroll          = optional_args[2] if len(optional_args) > 2 else None

            self.model.viewFDD(table, chain, outputFrmt, graphDir, unroll)
            self.console.appendToConsole(f"FDD for {table}/{chain} printed.")
        else:
            self.console.appendToConsole(f"FDD for {table}/{chain} not found.")

"""

def parse_file():
    try:
        global ruleset
        filename = input("Enter the filename to parse: ")
        # Select Parse Strategy
        iptables_strat = parser.IpTablesParser() # TODO Set parse strat
        # Create Parser Object
        parser_obj = parser.Parser(iptables_strat)
        # Parse File
        ruleset = parser_obj.parse(filename)
        print("File parsed successfully.")
    except Exception as e:
        print(f'Could not parse file. {e}')

def display_rules():
    try:
        if not ruleset:
            print("No ruleset parsed yet. Please parse a file first.")
            return
        table = input("Enter table name: ")
        chain = input("Enter chain name: ")

        print(ruleset[table][chain])
    except Exception as e:
        print(f'Could not Display rules: {e}')

def add_field_list():
    try:
        global field_list
        config_file = input("Enter config file path: ")
        # Create FieldList Object
        field_list = FieldList()
        # Load Config
        field_list.loadConfig(config_file)
        print("Field list added successfully.")
    except Exception as e:
        print(f'Could not add FieldList. {e}')

def generate_fdds():
    try:
        global fdds, ruleset, field_list
        if not ruleset or not field_list:
            print("Ruleset or field list not set. Please parse a file and add field list first.")
            return
        
        for table in ruleset.getTables():
            fdds[table] = {}
            for chain in ruleset[table].getChains():
                if len(ruleset[table][chain].getRules()) != 0: 
                    fdd = FDD(field_list)
                    fdd.genFDD(ruleset[table][chain])
                    fdds[table][chain] = fdd

        print("FDDs generated successfully.")
    except Exception as e:
        print(f'Could not generate FDD. {e}')

def compile_fdd():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    # Execute Reduction and Marking
    if table in fdds and chain in fdds[table]:
        fdds[table][chain].reduction()
        fdds[table][chain].marking()
        print(f"FDD for {table}/{chain} compiled successfully.")
    else:
        print(f"FDD for {table}/{chain} not found.")

def generate_optimized_ruleset():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    if table in fdds and chain in fdds[table]:
        optimized_ruleset = fdds[table][chain].firewallGen()
        print("Optimized ruleset generated:")
        print(optimized_ruleset)
    else:
        print(f"FDD for {table}/{chain} not found.")

def print_fdd():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    if table in fdds and chain in fdds[table]:
        name = input("Enter output file name: ")
        format = input("Enter output format (default: svg): ") or 'svg'
        fdds[table][chain].printFDD(name, format)
        print(f"FDD for {table}/{chain} printed to {name}.{format}")
    else:
        print(f"FDD for {table}/{chain} not found.")


"""