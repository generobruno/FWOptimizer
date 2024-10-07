"""_summary_

Raises:
    IndexError: _description_

Returns:
    _type_: _description_
"""

import os
from PyQt6 import QtCore, QtGui, QtWidgets
from views.mainView import Ui_MainWindow
import views.dialogs as Dialogs

class FWOView(QtWidgets.QMainWindow):
    """
    Top Module of the App View

    Args:
        QtWidgets (QtMainWindow): Main Window
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.startUpState()
        self.setUpFunctions()

    def startUpState(self):
        """
        Set up GUI Initial State
        """
        # TODO Display projects window
        
        # Hide side Menues
        self.ui.leftMenuContainer.collapse()
        self.ui.centerMenuContainer.hide()
        self.ui.rightMenuContainer.hide()
        self.ui.consoleContainer.hide()

    def setUpFunctions(self):
        """
        Set up the GUI Buttons Functions
        """
        # Connect actions to show the right menu and display the appropriate page
        self.ui.actionView_Imported_Rules.triggered.connect(
            lambda: (
                self.ui.rightMenuContainer.setVisible(not self.ui.rightMenuContainer.isVisible()) or self.ui.rightMenuStack.setCurrentWidget(self.ui.importedPage),
                self.ui.label_5.setText("Imported Rules")
            )
        )
        self.ui.actionView_Exported_Rules.triggered.connect(
            lambda: (
                self.ui.rightMenuContainer.setVisible(not self.ui.rightMenuContainer.isVisible()) or self.ui.rightMenuStack.setCurrentWidget(self.ui.exportedPage),
                self.ui.label_5.setText("Exported Rules")
            )
        )
        # Create a shortcut for "Ctrl+I" or "Ctrl+E" to toggle the right menu visibility
        self.ui.actionView_Imported_Rules.setShortcut(QtGui.QKeySequence("Ctrl+I"))
        self.ui.actionView_Exported_Rules.setShortcut(QtGui.QKeySequence("Ctrl+E"))
        # Close right Menu
        self.ui.closeRightMenuBtn.clicked.connect(
            lambda: self.ui.rightMenuContainer.setVisible(False)
        )
        
        # Toggle left Menu
        self.ui.leftMenuBtn.clicked.connect(
            lambda: self.ui.leftMenuContainer.toggle()
        )
        
        # Expand Center Menu Widget
        self.ui.homeBtn.clicked.connect(
            lambda: (
                self._togglePage(2),
                self.ui.label.setText("Home")
            )
        )
        self.ui.settingsBtn.clicked.connect(
            lambda: (
                self._togglePage(0),
                self.ui.label.setText("Settings")
            )
        )
        self.ui.rulesBtn.clicked.connect(
            lambda: (
                self._togglePage(1),
                self.ui.label.setText("Imported Rules")
            )
        )
        self.ui.reportsBtn.clicked.connect(
            lambda: (
                self._togglePage(3),
                self.ui.label.setText("Reports")
            )
        )
        # Close Center Menu Widget
        self.ui.closeCenterMenuBtn.clicked.connect(
            lambda: self.ui.centerMenuContainer.setVisible(False)
        )
        
        # Expand Bottom Menu Widget
        self.ui.consoleBtn.clicked.connect(
            lambda: self.ui.consoleContainer.setVisible(not self.ui.consoleContainer.isVisible())
        )
        self.ui.consoleBtn.setShortcut(QtGui.QKeySequence("Ctrl+J"))
        
        # Help Button
        self.ui.helpBtn.clicked.connect(
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/generobruno/FWOptimizer'))
        )

    def _togglePage(self, pageIndex):
        """
        Toggle the center Menu page index

        Args:
            pageIndex (int): Index of the Page
        """
        if self.ui.centerMenuStack.currentIndex() == pageIndex:
            self.ui.centerMenuContainer.setVisible(not self.ui.centerMenuContainer.isVisible())
        else:
            self.ui.centerMenuContainer.setVisible(True)
            self.ui.centerMenuStack.setCurrentIndex(pageIndex)

    def displayImportedRulesTab(self):
        """
        Show the imported Rules tab
        """
        self._togglePage(1)
        self.ui.label.setText("Imported Rules")

    def displayImportedRules(self, content, rulesParsed):
        """
        Display the parsed rules in the QTreeView and right menu.
        
        Args:
            content: Rules as text to display in right menu
            rulesParsed: The parsed rules to display in left menu.
        """
        # Create a QStandardItemModel
        treeView = QtGui.QStandardItemModel()
        treeView.setHorizontalHeaderLabels(["Policy", "Details"])
        self.ui.treePoliciesView.setStyleSheet("""
            QHeaderView::section {
                background-color: #2c313c;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
                border-radius: 8px;
            }
        """)

        # Iterate over the tables in the RuleSet
        for tableName, table in rulesParsed.getTables().items():
            tableItem = QtGui.QStandardItem(f"Table: {tableName}")
            tableItem.setEditable(False)

            # Iterate over the chains in the table
            for chainName, chain in table.getChains().items():
                chainItem = QtGui.QStandardItem(f"Chain: {chainName}")
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
        
        # Resize columns to fit contents
        for column in range(treeView.columnCount()):
            self.ui.treePoliciesView.resizeColumnToContents(column)
        
        # Set imported rules right menu
        self.ui.importedRules.setText(content)
        self.ui.rightMenuStack.setCurrentWidget(self.ui.importedPage)
        
        self.displayImportedRulesTab()
        
    def displayExportedRules(self, content):
        """
        Display the parsed rules in the right menu.
        
        Args:
            content: Rules as text to display in right menu
        """
        #TODO Also display on centerMenu as RuleSet?
        # Set exported rules right menu
        self.ui.exportedRules.setText(str(content))
        self.ui.rightMenuStack.setCurrentWidget(self.ui.exportedPage)
     
    def displayWorkingDirectoryTree(self, directory):
        """
        Display the working directory's files and folders in the QTreeView.
        
        Args:
            directory: Path to the working directory.
        """
        # Create a QStandardItemModel for the QTreeView
        treeView = QtGui.QStandardItemModel()
        treeView.setHorizontalHeaderLabels(["File/Folder", "Details"])
        self.ui.treeWorkdirView.setStyleSheet("""
            QHeaderView::section {
                background-color: #2c313c;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
                border-radius: 8px;
            }
        """)

        # Recursive function to add items to the tree view
        def addTreeItems(parentItem, path):
            for item in os.listdir(path):
                itemPath = os.path.join(path, item)
                itemNode = QtGui.QStandardItem(item)
                itemNode.setEditable(False)
                
                if os.path.isdir(itemPath):
                    detailsNode = QtGui.QStandardItem("Folder")
                    addTreeItems(itemNode, itemPath)  # Recursively add folder contents
                else:
                    detailsNode = QtGui.QStandardItem(f"File - {os.path.getsize(itemPath)} bytes")
                
                parentItem.appendRow([itemNode, detailsNode])

        # Add the root directory to the tree view
        rootItem = QtGui.QStandardItem(os.path.basename(directory))
        rootItem.setEditable(False)
        treeView.appendRow([rootItem, QtGui.QStandardItem("Root Folder")])

        # Add the contents of the directory
        addTreeItems(rootItem, directory)

        # Set the model to the QTreeView
        self.ui.treeWorkdirView.setModel(treeView)
        self.ui.treeWorkdirView.expandAll()

        # Resize columns to fit contents
        for column in range(treeView.columnCount()):
            self.ui.treeWorkdirView.resizeColumnToContents(column) 
            
    def displayWarningMessage(self, message: str):
        """
        Display custom warning message

        Args:
            message (str): Message to display
        """
        QtWidgets.QMessageBox.warning(self, "Warning", message)
        return
    
    def displayErrorMessage(self, message: str):
        """
        Display custom error message

        Args:
            message (str): Message to display
        """
        QtWidgets.QMessageBox.critical(self, "Error", message)
        return
    
    def displayInfoMessage(self, title:str, message:str):
        """
        Display custom information message

        Args:
            message (str): Message to display
        """
        QtWidgets.QMessageBox.information(self, title, message)
        return
    
    def selectFileDialog(self, filterFiles="All Files (*)"):
        """
        User selects a file path

        Args:
            filterFiles (str, optional): Files to filter (separate with ";;"). 
            Defaults to "All Files (*)".

        Returns:
            str: File path
        """
        options = QtWidgets.QFileDialog.Option.ReadOnly
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=None,
            caption="Import Rules File",
            directory="",
            filter=filterFiles,
            options=options
        )
        
        return filePath
    
    def selectFddDialog(self, tables):
        """
        Show Dialog to select the chain to generate, or all the firewall.

        Args:
            chains (_type_): _description_

        Returns:
            str: Option selected
        """
        dialog = Dialogs.SelectFDDDialog(tables=tables, parent=self)
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
        dialog = Dialogs.ViewFDDDialog(tables=tables, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return dialog.getSelectedOptions()
        return None
    
    def exportRulesDialog(self, tables):
        """
        Show Dialog to select the chain to generate, or all the firewall.
        Also allow the user to specify the file name and folder to store the generated file.

        Args:
            tables (dict): A dictionary containing tables and chains.

        Returns:
            tuple: (option, file_path) where option can be "all" or (table_name, chain_name),
                and file_path is the directory and file name specified by the user.
        """
        dialog = Dialogs.ExportRulesDialog(tables=tables, parent=self)
        
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            option = dialog.getSelectedOption()

            if option:
                # Ask the user to specify the file name and select a directory to save the file
                file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                    parent=None,
                    caption="Save Exported Rules",
                    directory="",
                    filter="Text Files (*.txt);;All Files (*)"
                )

                if file_path:
                    return option, file_path
        
        return None, None
    
    def saveProjectDialog(self):
        """
        Allow the user to specify the file name and folder to store the project.

        Returns:
            Directory and file name specified by the user to save the project. None if an error occurred.
        """

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=None,
            caption="Save Project",
            directory="",
            filter="FWO Files (*.fwo)"
        )

        if filePath:
            # Ensure the file has the correct extension
            if not filePath.endswith(".fwo"):
                filePath += ".fwo"
            return filePath
        
        return None
                
    def showLoadingIndicator(self, opt: bool=True):
        """
        Display the loading spinner,

        Args:
            opt (bool, optional): Display if True, else Hide. Defaults to True.
        """
        if opt:
            self.ui.loading.start()
        else:
            self.ui.loading.stop()
            
    def showCloseConfirmationDialog(self, title:str, message:str):
        """
        Display close confirmation dialog

        Returns:
            bool: True is user selected Yes, False otherwise.
        """
        reply = QtWidgets.QMessageBox.warning(
            self, title,
            message,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Cancel,
            QtWidgets.QMessageBox.StandardButton.Cancel
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        elif reply == QtWidgets.QMessageBox.StandardButton.No:
            return False
        elif reply == QtWidgets.QMessageBox.StandardButton.Cancel:
            return None
                