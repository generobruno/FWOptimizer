from PyQt6 import QtCore, QtGui, QtWidgets
from views.mainView import Ui_MainWindow
from views.dialogs import SelectFDDDialog, ViewFDDDialog

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
        
    def displayErrorMessage(self, message: str):
        """
        Display custom error message

        Args:
            message (str): Message to display
        """
        QtWidgets.QMessageBox.warning(self, "Error", message)
        return
    
    def selectFddDialog(self, tables):
        """
        Show Dialog to select the chain to generate, or all the firewall.

        Args:
            chains (_type_): _description_

        Returns:
            str: Option selected
        """
        dialog = SelectFDDDialog(tables=tables, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            option = dialog.getSelectedOption()
            if option == "all":
                return option
            elif option[0] == "specific":
                return option[1]
                #TODO Manejar erro NoneType cuando selecciono la tabla sin querer
    
    def selectViewFddDialog(self, tables):
        """
        Show Dialog to select the chain and options to view the FDD.

        Args:
            tables (dict): Dictionary of tables and their chains.

        Returns:
            tuple: Option selected (table_name, chain_name), image_format, graph_orientation, unroll_decisions
        """
        dialog = ViewFDDDialog(tables=tables, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return dialog.getSelectedOptions()
        return None
    