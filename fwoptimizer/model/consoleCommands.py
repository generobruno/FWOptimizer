"""_summary_
"""

import model.fwoManager as fwm
import views.customWidgets as cw

class ConsoleCommands:
    """
    Console Emulator for the user interaction with the model.
    """
    def __init__(self, model: fwm.FWOManager, console: cw.ConsoleWidget):
        self.model = model
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
        """_summary_

        Args:
            args (_type_): _description_
        """
        pass

    def displayRules(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        pass
    
    def addFieldList(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        pass
    
    def generateFdds(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        pass
    
    def optimizeFdds(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
        pass
    
    def exportRules(self, args):
        """_summary_

        Args:
            args (_type_): _description_
        """
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