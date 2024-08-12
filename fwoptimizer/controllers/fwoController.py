from model.fwoManager import FWOManager
from views.fwoView import FWOView

from PyQt6 import QtCore, QtGui, QtWidgets

class FWOController:
    def __init__(self, model: FWOManager, view: FWOView):
        self.model = model
        self.view = view
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
        self.model.setFieldList()
    
    def importRules(self):
        """
        Import Rules and save them in the Right Menu
        """
        fileContent, rules = self.model.importRules()
        if fileContent and rules:
            self.view.displayImportedRules(fileContent, rules)
            
    def generateFDD(self):
        """
        Generate an FDD
        """
        if self.model.currentFirewall.getFieldList() is None:
            self.view.displayErrorMessage("No Field List loaded.\nPlease import it first.")
            return

        if not self.model.currentFirewall or not self.model.currentFirewall.inputRules:
            self.view.displayErrorMessage("No rules loaded.\nPlease import rules first.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.inputRules.getTables()

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
        tables = self.model.currentFirewall.inputRules.getTables()

        options = self.view.selectViewFddDialog(tables)
        
        if options:
            (table_name, chain_name), image_format, graph_orientation, unroll_decisions = options
            print(f"Viewing FDD for {table_name} -> {chain_name}:\n{image_format} format, {graph_orientation} orientation, Unroll Decisions: {unroll_decisions}")
            self.model.viewFDD(
                table=table_name, 
                chain=chain_name, 
                imgFormat=image_format, 
                graphDir=graph_orientation, 
                unrollDecisions=unroll_decisions
            )
            
    def optimizeFDD(self):
        """
        Optimize the FDD
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayErrorMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.inputRules.getTables()

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
        tables = self.model.currentFirewall.inputRules.getTables()

        # User selects option to generate
        option = self.view.selectFddDialog(tables)
        
        # Generate rules given user selection
        if option == "all":  
            exportedRules = self.model.exportRules()
        elif isinstance(option, tuple):
            tableName, chainName = option
            exportedRules = self.model.exportRules(tableName, chainName)
        else:
            self.view.displayErrorMessage("No valid option selected for FDD generation.")
        
        # Generate export File from RuleSet, given the Parser Strategy
        fileContent = self.model.getParserStrategy().compose(exportedRules)
        
        # Save exported rules to right menu 
        if fileContent:
            self.view.displayExportedRules(fileContent)