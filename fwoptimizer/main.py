"""_summary_
"""

import sys
import os
from PyQt6 import QtWidgets, QtCore

# Add Root Dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.fwoManager import FWOManager
from views.fwoView import FWOView
from controllers.fwoController import FWOController

class FWOptimizer:
    """
    Main Application
    """
    def __init__(self, sys_argv):
        self.app = QtWidgets.QApplication(sys_argv)
        
        self.model = FWOManager()
        self.view = FWOView()
        self.controller = FWOController(self.model, self.view)

        # Connect the aboutToQuit signal
        self.app.aboutToQuit.connect(self.cleanUp)
        
        self.view.show()
        
        #self.controller.startUp() #TODO StartUp

    def run(self):
        return self.app.exec()
    
    def cleanUp(self):
        if hasattr(self.controller, 'cleanUp'):
            self.controller.cleanUp()


if __name__ == '__main__':
    
    app = FWOptimizer(sys.argv)
    
    try:
        exit_code = app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit_code = 1
    finally:
        sys.exit(exit_code)