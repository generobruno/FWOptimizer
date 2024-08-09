from model.fwoManager import FWOManager
from views.fwoView import FWOView

class FWOController:
    def __init__(self, model: FWOManager, view: FWOView):
        self.model = model
        self.view = view
        self.connectSignals()
        
    def connectSignals(self):
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
        
    def importRules(self):
        """
        Import Rules and save them in the Right Menu
        """
        file_content = self.model.importRules()
        if file_content:
            self.view.displayImportedRules(file_content)