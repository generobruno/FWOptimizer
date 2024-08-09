from PyQt6 import QtWidgets
from views.mainView import Ui_MainWindow

class FWOView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
    def setUpFunctions(self):
        self.ui.setUpFunctions()
        
    def displayImportedRules(self, content):
        self.ui.importedRules.setText(content)
        self.ui.rightMenuStack.setCurrentWidget(self.ui.importedPage)