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
        self.app.aboutToQuit.connect(self.cleanUp) #TODO Remove work folder if not saved
        
        self.view.show()
        
        #self.controller.startUp()

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

"""
from classes import *

if __name__ == '__main1__':

    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./fwo_workdir/inputs/iptables-save-example.txt")
    
    firewall = Firewall(defaultWorkFolder='test_wd')
    firewall.setFieldList("fwoptimizer/configs/fdd_config.toml")
    firewall.setInputRules(rules_parsed)
    
    firewall.genFdd('filter', 'excepciones-in')
    
    #firewall.optimizeFdd('filter', 'excepciones-in')
    
    fdd: FDD = firewall.getFDD('filter','excepciones-in')

    fdd.clearFilters()
    
    #print(f'ALL FDDLIST: {firewall.getFDDs()}')

    print(f"filter: dst 8008: {fdd.filterFDD('DstPort', '8008')}")

    fdd.printFDD('example','svg')

    print(f"filter: prot tcp: {fdd.filterFDD('Protocol', 'tcp')}")

    fdd.printFDD('example2','svg')

    print(f"filter: srcip: {fdd.filterFDD('SrcIP', '190.30.247.90/32')}")

    fdd.printFDD('example3','svg')

    
    
    #print(f'FIREWALL FIELDLIST: {[f.getName() for f in firewall.getFieldList().getFields()]}')
    
    # output_rules = firewall.genOutputRules('filter', 'INPUT')
    
    #print(f'PARSER OUTPUT:\n{parser.compose(output_rules)}')
"""