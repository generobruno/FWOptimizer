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
if __name__ == '__main2__':

    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./.example_set_C.txt")

    chain1 = rules_parsed['filter']['INPUT']
    print("Chain1:")
    for rule in chain1:
        print(rule)

    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    rules_parsed = parser.parse("./.example_set_D.txt")

    chain2 = rules_parsed['filter']['INPUT']
    print("Chain2:")
    for rule in chain2:
        print(rule)

    # fdd = FDD(fieldList)
    # fdd.genFDD(chain1)
    # #fdd.printFDD("FDD", 'svg')

    # fdd.reduction()
    # #fdd.printFDD("reducedFDD")
    
    # fdd.marking()
    # #fdd.printFDD("MarkedFDD", 'svg')
    
    # firewall_chain = fdd.firewallGen()
    # firewall_chain.setDefaultDecision("DROP") 

    #print(firewall_chain)

    comparator = ChainComparator(fieldList)
    comparator.setChain1FromChain(chain1)
    comparator.setChain2FromChain(chain2)
    print(f"{comparator}")
    print(f"\nLa comparacion entre chain1 y chain2 da: {comparator.areEquivalents()}")
"""