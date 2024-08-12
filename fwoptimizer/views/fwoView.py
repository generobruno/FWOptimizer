from PyQt6 import QtCore, QtGui, QtWidgets
from views.mainView import Ui_MainWindow

class FWOView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startUpState()
        self.ui.setUpFunctions()

    def displayImportedRules(self, content, rulesParsed):
        """
        Display the parsed rules in the QTreeView.
        
        Args:
            content: Rules as text to display in right menu
            rulesParsed: The parsed rules to display in left menu.
        """
        # Create a QStandardItemModel
        treeView = QtGui.QStandardItemModel()
        treeView.setHorizontalHeaderLabels(["Policy", "Details"])

        # Iterate over the tables in the RuleSet
        for tableName, table in rulesParsed.getTables().items():
            tableItem = QtGui.QStandardItem(f"Table:\t {tableName}")
            tableItem.setEditable(False)

            # Iterate over the chains in the table
            for chainName, chain in table.getChains().items():
                chainItem = QtGui.QStandardItem(f"Chain:\t {chainName}")
                chainItem.setEditable(False)

                # Iterate over the rules in the chain
                for rule in chain.getRules():
                    ruleItem = QtGui.QStandardItem(f"Rule ID: {rule.getId()}")
                    ruleItem.setEditable(False)

                    # Create a string with predicates and decision
                    details = []

                    # Add predicates to the details
                    for option, value in rule.getPredicates().items():
                        details.append(f"{option} = {value}")
                    
                    # Add decision to the details
                    details.append(f"Decision: {rule.getDecision()}")

                    detailsStr = "\n".join(details)
                    detailsItem = QtGui.QStandardItem(detailsStr)
                    detailsItem.setEditable(False)

                    # Add the rule and its details to the chain item
                    chainItem.appendRow([ruleItem, detailsItem])

                tableItem.appendRow(chainItem)

            treeView.appendRow(tableItem)

        # Set the model to the QTreeView
        self.ui.treePoliciesView.setModel(treeView)
        self.ui.treePoliciesView.expandAll()
        
        # Set imported rules right menu
        self.ui.importedRules.setText(content)
        self.ui.rightMenuStack.setCurrentWidget(self.ui.importedPage)