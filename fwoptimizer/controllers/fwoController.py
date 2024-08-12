from model.fwoManager import FWOManager
from views.fwoView import FWOView

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
        view.exportBtn.clicked.connect(model.exportRules)
        view.actionExport_Policy.triggered.connect(model.exportRules)
        
        view.generateBtn.clicked.connect(model.generateFDD)
        
        view.optimizeBtn.clicked.connect(model.optimizeFDD)
        
        # Pass the QGraphicsView reference to the model
        model.setGraphicsView(view.graphicsView)
        view.viewBtn.clicked.connect(model.viewFDD)
        
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
    
    def importRules(self):
        """
        Import Rules and save them in the Right Menu
        """
        fileContent, rules = self.model.importRules()
        if fileContent and rules:
            self.view.displayImportedRules(fileContent, rules)