from PyQt6 import QtWidgets, QtGui

class SelectFDDDialog(QtWidgets.QDialog):
    def __init__(self, tables=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate FDD")
        self.setModal(True)

        # Radio buttons for selecting generation options
        self.allChainsRadio = QtWidgets.QRadioButton("Generate FDDs for all chains")
        self.specificChainRadio = QtWidgets.QRadioButton("Generate FDD for a specific Chain")
        self.specificChainRadio.setChecked(True)

        # Tree view for selecting a specific chain
        self.chainTreeView = QtWidgets.QTreeWidget()
        self.chainTreeView.setHeaderLabel("Tables and Chains")
        
        if tables:
            for table_name, table in tables.items():
                table_item = QtWidgets.QTreeWidgetItem(self.chainTreeView)
                table_item.setText(0, table_name)
                
                for chain_name, _ in table.getChains().items():
                    chain_item = QtWidgets.QTreeWidgetItem(table_item)
                    chain_item.setText(0, chain_name)
        
        self.chainTreeView.expandAll()
        
        # Button box for OK and Cancel
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Layout setup
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.allChainsRadio)
        layout.addWidget(self.specificChainRadio)
        layout.addWidget(self.chainTreeView)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        # Connecting signals
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getSelectedOption(self):
        if self.allChainsRadio.isChecked():
            return "all"
        elif self.specificChainRadio.isChecked():
            selected_item = self.chainTreeView.currentItem()
            if selected_item and selected_item.parent():
                table_name = selected_item.parent().text(0)
                chain_name = selected_item.text(0)
                return "specific", (table_name, chain_name)
            else:
                return None
        return None
    
class ViewFDDDialog(QtWidgets.QDialog):
    def __init__(self, tables=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View FDD")
        self.setModal(True)

        # Radio button for selecting specific chain
        self.specificChainRadio = QtWidgets.QRadioButton("View FDD for a specific Chain")
        self.specificChainRadio.setChecked(True)

        # Tree view for selecting a specific chain
        self.chainTreeView = QtWidgets.QTreeWidget()
        self.chainTreeView.setHeaderLabel("Tables and Chains")
        
        if tables:
            for table_name, table in tables.items():
                table_item = QtWidgets.QTreeWidgetItem(self.chainTreeView)
                table_item.setText(0, table_name)
                
                for chain_name, _ in table.getChains().items():
                    chain_item = QtWidgets.QTreeWidgetItem(table_item)
                    chain_item.setText(0, chain_name)
        
        self.chainTreeView.expandAll()

        # Dropdown for image format selection
        self.imageFormatLabel = QtWidgets.QLabel("Image Format:")
        self.imageFormatComboBox = QtWidgets.QComboBox()
        self.imageFormatComboBox.addItems(['svg', 'png', 'jpeg'])
        self.imageFormatComboBox.setCurrentText('svg')

        # Dropdown for graph orientation selection
        self.graphOrientationLabel = QtWidgets.QLabel("Graph Orientation:")
        self.graphOrientationComboBox = QtWidgets.QComboBox()
        self.graphOrientationComboBox.addItems(['TB', 'BT', 'LR', 'RL'])
        self.graphOrientationComboBox.setCurrentText('TB')

        # Checkbox for unrolling decisions
        self.unrollDecisionsLabel = QtWidgets.QLabel("Unroll Decisions:")
        self.unrollDecisionsCheckBox = QtWidgets.QCheckBox()
        self.unrollDecisionsCheckBox.setChecked(False)

        # Button box for OK and Cancel
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Layout setup
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.specificChainRadio)
        layout.addWidget(self.chainTreeView)
        layout.addWidget(self.imageFormatLabel)
        layout.addWidget(self.imageFormatComboBox)
        layout.addWidget(self.graphOrientationLabel)
        layout.addWidget(self.graphOrientationComboBox)
        layout.addWidget(self.unrollDecisionsLabel)
        layout.addWidget(self.unrollDecisionsCheckBox)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        # Connecting signals
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getSelectedOptions(self):
        if self.specificChainRadio.isChecked():
            selected_item = self.chainTreeView.currentItem()
            if selected_item and selected_item.parent():
                table_name = selected_item.parent().text(0)
                chain_name = selected_item.text(0)
                image_format = self.imageFormatComboBox.currentText()
                graph_orientation = self.graphOrientationComboBox.currentText()
                unroll_decisions = self.unrollDecisionsCheckBox.isChecked()
                return (table_name, chain_name), image_format, graph_orientation, unroll_decisions
        return None

class ExportRulesDialog(QtWidgets.QDialog):
    def __init__(self, tables=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Rules")
        self.setModal(True)

        # Radio buttons for selecting export options
        self.allChainsRadio = QtWidgets.QRadioButton("Export rules for all chains")
        self.specificChainRadio = QtWidgets.QRadioButton("Export rules for a specific Chain")
        self.specificChainRadio.setChecked(True)

        # Tree view for selecting a specific chain
        self.chainTreeView = QtWidgets.QTreeWidget()
        self.chainTreeView.setHeaderLabel("Tables and Chains")
        
        if tables:
            for table_name, table in tables.items():
                table_item = QtWidgets.QTreeWidgetItem(self.chainTreeView)
                table_item.setText(0, table_name)
                
                for chain_name, _ in table.getChains().items():
                    chain_item = QtWidgets.QTreeWidgetItem(table_item)
                    chain_item.setText(0, chain_name)
        
        self.chainTreeView.expandAll()

        # Button box for OK and Cancel
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Layout setup
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.allChainsRadio)
        layout.addWidget(self.specificChainRadio)
        layout.addWidget(self.chainTreeView)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        # Connecting signals
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getSelectedOption(self):
        if self.allChainsRadio.isChecked():
            return "all"
        elif self.specificChainRadio.isChecked():
            selected_item = self.chainTreeView.currentItem()
            if selected_item and selected_item.parent():
                table_name = selected_item.parent().text(0)
                chain_name = selected_item.text(0)
                return (table_name, chain_name) 
            else:
                return None
        return None
    
class FileViewerDialog(QtWidgets.QDialog):
    def __init__(self, filePath, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{filePath}")
        self.setMinimumSize(600, 400)
        
        # Main layout for the dialog
        layout = QtWidgets.QVBoxLayout(self)

        # Create a QTextEdit widget to display the file content
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setReadOnly(True)

        # Read and display the file content
        self.loadFile(filePath)

        # Create a horizontal layout for search functionality
        searchLayout = QtWidgets.QHBoxLayout()

        # Create a QLineEdit for entering search terms
        self.searchInput = QtWidgets.QLineEdit(self)
        self.searchInput.setPlaceholderText("Search...")
        self.searchInput.setClearButtonEnabled(True)

        # Create a label for search results count
        self.searchResultLabel = QtWidgets.QLabel(self)

        # Connect search functionality
        self.searchInput.textChanged.connect(self.search)

        # Add the search input and result label to the search layout
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchResultLabel)

        # Add the search layout and text edit to the main layout
        layout.addLayout(searchLayout)
        layout.addWidget(self.textEdit)

        # Add a close button
        closeButton = QtWidgets.QPushButton("Close", self)
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton)

    def loadFile(self, filePath):
        """
        Load the file content and display it in the QTextEdit.
        """
        try:
            with open(filePath, 'r') as file:
                fileContent = file.read()
                self.textEdit.setText(fileContent)
        except Exception as e:
            self.textEdit.setText(f"Error opening file: {e}")

    def search(self):
        """
        Search, highlight occurrences of the search term, and show result count.
        """
        searchTerm = self.searchInput.text()

        # Clear previous formatting
        self.clearHighlights()

        if searchTerm:
            # Create a QTextCursor to traverse the document
            cursor = self.textEdit.textCursor()
            cursor.setPosition(0)

            # Define the formatting to highlight text
            highlightFormat = QtGui.QTextCharFormat()
            highlightFormat.setBackground(QtGui.QColor("yellow"))
            highlightFormat.setForeground(QtGui.QColor("black"))

            highlightCount = 0

            # Find and highlight all occurrences
            while True:
                cursor = self.textEdit.document().find(searchTerm, cursor, QtGui.QTextDocument.FindFlag.FindWholeWords)
                
                if cursor.isNull():
                    self.clearHighlights()
                    break

                highlightCount += 1
                # Set the format on the matched text
                cursor.mergeCharFormat(highlightFormat)

            # Scroll to the first occurrence if found
            if highlightCount > 0:
                self.textEdit.setTextCursor(cursor)

            # Update the result label
            self.searchResultLabel.setText(f"{highlightCount} result(s) found.")
        else:
            self.searchResultLabel.setText("")

    def clearHighlights(self):
        """
        Remove all highlights by resetting the formatting for the entire document.
        """
        # Select the entire document
        cursor = self.textEdit.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.Document)
        
        # Apply default formatting (clears highlights)
        defaultFormat = QtGui.QTextCharFormat()
        cursor.setCharFormat(defaultFormat)
