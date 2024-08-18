"""_summary_

Raises:
    IndexError: _description_

Returns:
    _type_: _description_
"""

from model.fwoManager import FWOManager
from views.fwoView import FWOView
from model.consoleCommands import ConsoleCommands

class FWOController:
    """
    App Controller for user interaction
    """
    def __init__(self, model: FWOManager, view: FWOView):
        self.model: FWOManager = model
        self.view: FWOView = view
        self.console = ConsoleCommands(self.model, self.view, self.view.ui.console)
        self.connectSignals()
        
    def connectSignals(self):
        """
        Connect the view's signals with the model functions
        """
        view = self.view.ui
        model = self.model
        
        # Connect buttons to model functions
        view.importBtn.clicked.connect(self.importRules)
        view.actionImport_Policy.triggered.connect(self.importRules)
        
        # Set FieldList Config
        view.actionSet_fieldList.triggered.connect(self.setFieldList)
        
        # Generate FDD Button
        view.generateBtn.clicked.connect(self.generateFDD)

        # Save Button
        view.actionSave_Project.triggered.connect(self.saveProyect)
        # Load Button
        view.actionLoad_Project.triggered.connect(self.loadProyect)
        
        # Pass the QGraphicsView reference to the model
        model.setGraphicsView(view.graphicsView)
        view.viewBtn.clicked.connect(self.viewFDD)
        
        # Optimize a FDD
        view.optimizeBtn.clicked.connect(self.optimizeFDD)
        
        # Generate and Export Rules optimized
        view.exportBtn.clicked.connect(self.exportRules)
        view.actionExport_Policy.triggered.connect(self.exportRules)
        
        # Connect the action to load parser syntax
        view.actionSet_parser.triggered.connect(self.setParserStrat)
        
        # Connect console commands
        view.console.commandEntered.connect(self.processCommand)
    
    def setParserStrat(self):
        """
        Select the parser Strategy
        """
        # TODO ask the user to choose a parser strategy, e.g., via a dialog
        #iptables_strat = parser.IpTablesParser()
        #parser_instance = parser.Parser(iptables_strat)
        #self.model.setParserStrategy(parser_instance)
        print("TODO: Parser strategy set.")
    
    def setFieldList(self):
        """
        Set the model's Field List
        """
        print("Setting Field List...")
        filePath = self.view.selectFileDialog("TOML Files (*.toml);;All Files (*)")
        
        if filePath:
            self.model.setFieldList(filePath)
        else:
            print("No file Selected.")
    
    def importRules(self):
        """
        Import Rules and save them in the Right Menu
        """
        filePath = self.view.selectFileDialog()
        
        if filePath:
            fileContent, rules = self.model.importRules(filePath)
            if fileContent and rules:
                self.view.displayImportedRules(fileContent, rules)
        else:
            print("No file Selected.")
            
    def generateFDD(self):
        """
        Generate an FDD
        """
        if self.model.currentFirewall.getFieldList() is None:
            self.view.displayErrorMessage("No Field List loaded.\nPlease import it first.")
            return

        if not self.model.currentFirewall or not self.model.currentFirewall._inputRules:
            self.view.displayErrorMessage("No rules loaded.\nPlease import rules first.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall._inputRules.getTables()

        # User selects option to generate
        option = self.view.selectFddDialog(tables)
        
        # Generate FDD given user selection
        if option == "all":  
            self.model.generateFDD()
        elif isinstance(option, tuple):
            tableName, chainName = option
            self.model.generateFDD(tableName, chainName)
        else:
            self.view.displayErrorMessage("No valid option selected for FDD generation.")
            
    def viewFDD(self):
        """
        Display the FDD
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayErrorMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return

        # Get all tables from the current firewall's RuleSet
        tables = self.model.currentFirewall.getInputRules().getTables()

        options = self.view.selectViewFddDialog(tables)
        
        if options:
            (tableName, chainName), imageFrmt, graphDir, unrollDecisions = options
            print(f"Viewing FDD for {tableName} -> {chainName}:\n{imageFrmt} format, {graphDir} orientation, Unroll Decisions: {unrollDecisions}")
            self.model.viewFDD(
                table=tableName, 
                chain=chainName, 
                imgFormat=imageFrmt, 
                graphDir=graphDir, 
                unrollDecisions=unrollDecisions
            )
            
    def optimizeFDD(self):
        """
        Optimize the FDD
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayErrorMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.getInputRules().getTables()

        # User selects option to generate
        option = self.view.selectFddDialog(tables)
        
        # Optimize FDD given user selection
        if option == "all":  
            self.model.optimizeFDD()
        elif isinstance(option, tuple):
            tableName, chainName = option
            self.model.optimizeFDD(tableName, chainName)
        else:
            self.view.displayErrorMessage("No valid option selected for FDD generation.")
            
    def exportRules(self):
        """
        Generate Rules and Export them to a file
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayErrorMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.getInputRules().getTables()

        # User selects option and file path
        option, filePath = self.view.exportRulesDialog(tables)
        
        if option and filePath:
            # Generate rules given user selection
            if option == "all":
                exportedRules = self.model.exportRules()
            elif isinstance(option, tuple):
                tableName, chainName = option
                print(f'Exporting specific - Table: {tableName}, Chain: {chainName}')
                exportedRules = self.model.exportRules(tableName, chainName)
            else:
                self.view.displayErrorMessage("No valid option selected for FDD generation.")
                return
            
            # Generate export File from RuleSet, given the Parser Strategy
            fileContent = self.model.getParserStrategy().compose(exportedRules)
            
            # Save exported rules to right menu 
            if fileContent:
                self.view.displayExportedRules(fileContent)
                
                # Write the file content to the specified file path
                with open(filePath, 'w') as file:
                    file.write(fileContent)
                
                print(f'Exported file to: {filePath}')
        else:
            self.view.displayErrorMessage("No valid option or file path selected for export.")

    def saveProyect(self):

        self.model.serializeFirewall()

    def loadProyect(self):

        self.model.deserializeFirewall()
            
    def processCommand(self, command):
        """
        Process a command entered in the console.

        Args:
            command (str): Command entered by the user
        """
        if command == 'exit':
            self.view.ui.consoleContainer.hide()
            self.view.ui.console.clear()
        else:
            self.console.executeCommand(command)
