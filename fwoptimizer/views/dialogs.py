from PyQt6 import QtWidgets, QtGui, QtCore
import fwoptimizer.views.resources_rc

class SelectFDDDialog(QtWidgets.QDialog):
    def __init__(self, tables=None, mode='Generate', parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate FDD")
        self.setModal(True)

        # Radio buttons for selecting generation options
        self.allChainsRadio = QtWidgets.QRadioButton(f"{mode} FDDs for all chains")
        self.specificChainRadio = QtWidgets.QRadioButton(f"{mode} FDD for a specific Chain")
        self.specificChainRadio.setChecked(True)

        # Tree view for selecting a specific chain
        self.chainTreeView = QtWidgets.QTreeWidget()
        self.chainTreeView.setHeaderLabel("Tables and Chains")
        
        if tables:
            for table_name, table in tables.items():
                table_item = QtWidgets.QTreeWidgetItem(self.chainTreeView)
                table_item.setText(0, table_name)
                table_item.setFlags(table_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
                
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
    def __init__(self, tables=None, fields=None, parent=None):
        super().__init__(parent)
        self.tables = tables
        self.fields = [f.getName() for f in fields]
        
        self.setWindowTitle("View or Filter FDD")
        self.setModal(True)
        self.styleDialog()

        # Create tab widget
        self.tabWidget = QtWidgets.QTabWidget(self)

        # Create View FDD tab
        self.viewFddTab = QtWidgets.QWidget()
        self.createViewFddTab(tables)

        # Create Filter FDD tab
        self.filterFddTab = QtWidgets.QWidget()
        self.createFilterFddTab(tables)

        # Add tabs to tab widget
        self.tabWidget.addTab(self.viewFddTab, "View FDD")
        self.tabWidget.addTab(self.filterFddTab, "Filter FDD")

        # Button box for OK and Cancel
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Layout setup
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabWidget)
        layout.addWidget(buttonBox)

        # Set layout for dialog
        self.setLayout(layout)

        # Connecting signals
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def createViewFddTab(self, tables):
        layout = QtWidgets.QVBoxLayout(self.viewFddTab)

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
                table_item.setFlags(table_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
                
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

        # Add components to the layout
        layout.addWidget(self.specificChainRadio)
        layout.addWidget(self.chainTreeView)
        layout.addWidget(self.imageFormatLabel)
        layout.addWidget(self.imageFormatComboBox)
        layout.addWidget(self.graphOrientationLabel)
        layout.addWidget(self.graphOrientationComboBox)
        layout.addWidget(self.unrollDecisionsLabel)
        layout.addWidget(self.unrollDecisionsCheckBox)

    def createFilterFddTab(self, tables):
        layout = QtWidgets.QVBoxLayout(self.filterFddTab)

        # Dropdown for selecting table
        self.tableNameLabel = QtWidgets.QLabel("Table Name:")
        self.tableNameComboBox = QtWidgets.QComboBox(self.filterFddTab)
        self.tableNameComboBox.addItems(tables.keys())

        # Dropdown for selecting chain
        self.chainNameLabel = QtWidgets.QLabel("Chain Name:")
        self.chainNameComboBox = QtWidgets.QComboBox(self.filterFddTab)

        # Populate chain options based on selected table
        self.tableNameComboBox.currentIndexChanged.connect(self.updateChains)
        self.updateChains(0)  # Initialize chain list for the first table

        # Field and match expression inputs
        self.fieldLabel = QtWidgets.QLabel("Field:")
        self.fieldInputComboBox = QtWidgets.QComboBox(self.filterFddTab)
        self.fieldInputComboBox.addItems(self.fields)

        self.matchExpressionLabel = QtWidgets.QLabel("Match Expression:")
        self.matchExpressionInput = QtWidgets.QLineEdit(self.filterFddTab)
        
        # Create a horizontal layout for image format, graph orientation, and unroll decisions
        optionsLayout = QtWidgets.QHBoxLayout()

        # Dropdown for image format selection
        self.fimageFormatLabel = QtWidgets.QLabel("Image Format:")
        self.fimageFormatComboBox = QtWidgets.QComboBox()
        self.fimageFormatComboBox.addItems(['svg', 'png', 'jpeg'])
        self.fimageFormatComboBox.setCurrentText('svg')
        optionsLayout.addWidget(self.fimageFormatLabel)
        optionsLayout.addWidget(self.fimageFormatComboBox)

        # Dropdown for graph orientation selection
        self.fgraphOrientationLabel = QtWidgets.QLabel("Graph Orientation:")
        self.fgraphOrientationComboBox = QtWidgets.QComboBox()
        self.fgraphOrientationComboBox.addItems(['TB', 'BT', 'LR', 'RL'])
        self.fgraphOrientationComboBox.setCurrentText('TB')
        optionsLayout.addWidget(self.fgraphOrientationLabel)
        optionsLayout.addWidget(self.fgraphOrientationComboBox)

        # Checkbox for unrolling decisions
        self.funrollDecisionsLabel = QtWidgets.QLabel("Unroll Decisions:")
        self.funrollDecisionsCheckBox = QtWidgets.QCheckBox()
        self.funrollDecisionsCheckBox.setChecked(False)
        optionsLayout.addWidget(self.funrollDecisionsLabel)
        optionsLayout.addWidget(self.funrollDecisionsCheckBox)
        
        # Checkbox to clear filters
        self.fclearFiltersLabel = QtWidgets.QLabel("Clear Previous Filters:")
        self.fclearFitlersCheckBox = QtWidgets.QCheckBox()
        self.fclearFitlersCheckBox.setChecked(False)
        optionsLayout.addWidget(self.fclearFiltersLabel)
        optionsLayout.addWidget(self.fclearFitlersCheckBox)

        # Add components to layout
        layout.addWidget(self.tableNameLabel)
        layout.addWidget(self.tableNameComboBox)
        layout.addWidget(self.chainNameLabel)
        layout.addWidget(self.chainNameComboBox)
        layout.addWidget(self.fieldLabel)
        layout.addWidget(self.fieldInputComboBox)
        layout.addWidget(self.matchExpressionLabel)
        layout.addWidget(self.matchExpressionInput)

        # Add the horizontal layout with the image format, orientation, and unroll options
        layout.addLayout(optionsLayout)

    def styleDialog(self):
        """
        Apply a custom style sheet for the dialog
        """
        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e; /* Dark background */
                color: #ffffff; /* White text */
            }
            QLabel {
                color: #dcdcdc; /* Light gray labels */
            }
            QTreeWidget {
                background-color: #3b3b3b; /* Darker tree background */
                color: #ffffff; /* White text for tree */
            }
            QComboBox, QLineEdit, QTreeWidget {
                border: 1px solid #5a5a5a; /* Gray borders for inputs */
                padding: 5px;
            }
            QPushButton {
                background-color: #4e4e4e; /* Darker buttons */
                color: #ffffff; /* White text on buttons */
                border: 1px solid #5a5a5a;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5a5a5a; /* Lighter button when hovered */
            }
            QTabWidget::pane {
                border: 1px solid #5a5a5a; /* Border for tabs */
            }
            QTabBar::tab {
                background-color: #3b3b3b; /* Darker tab background */
                color: #dcdcdc; /* Light gray text for tabs */
                padding: 5px;
            }
            QTabBar::tab:selected {
                background-color: #4e4e4e; /* Selected tab background */
                color: #ffffff; /* White text for selected tab */
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                background-color: #ffffff; /* White background for checkbox indicator */
                border: 1px solid #5a5a5a;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #4e4e4e; /* Darker color when checked */
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #e0e0e0; /* Light gray on hover */
            }
        """)

    def updateChains(self, index):
        """ Update chain names based on selected table """
        table_name = self.tableNameComboBox.currentText()
        table = self.tables.get(table_name)
        self.chainNameComboBox.clear()
        if table:
            self.chainNameComboBox.addItems(table.getChains().keys())

    def getSelectedOptions(self):
        """ Determine which options to retrieve based on the active tab """
        active_tab_index = self.tabWidget.currentIndex()

        if active_tab_index == 0:  # View FDD tab
            if self.specificChainRadio.isChecked():
                selected_item = self.chainTreeView.currentItem()
                if selected_item and selected_item.parent():
                    table_name = selected_item.parent().text(0)
                    chain_name = selected_item.text(0)
                    image_format = self.imageFormatComboBox.currentText()
                    graph_orientation = self.graphOrientationComboBox.currentText()
                    unroll_decisions = self.unrollDecisionsCheckBox.isChecked()
                    return "viewFDD", (table_name, chain_name), image_format, graph_orientation, unroll_decisions
        elif active_tab_index == 1:  # Filter FDD tab
            table_name = self.tableNameComboBox.currentText()
            chain_name = self.chainNameComboBox.currentText()
            image_format = self.fimageFormatComboBox.currentText()
            graph_orientation = self.fgraphOrientationComboBox.currentText()
            unroll_decisions = self.funrollDecisionsCheckBox.isChecked()
            field = self.fieldInputComboBox.currentText()
            match_expression = self.matchExpressionInput.text()
            clear_filters = self.fclearFitlersCheckBox.isChecked()
            return "filterFDD", table_name, chain_name, (image_format, graph_orientation, unroll_decisions), field, match_expression, clear_filters
        
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

class AddRulesDialog(QtWidgets.QDialog):
    def __init__(self, tables, fields, decisions, parent=None):
        super().__init__(parent)
        self.tables = tables
        self.fields = [f.getName() for f in fields]  # List of all possible predicate fields
        self.used_predicates = set()  # Track predicates already added to avoid duplicates

        self.setWindowTitle("Add Rule")
        self.setModal(True)
        self.resize(600, 200)  # Set initial width and height

        self.styleDialog()

        # FDD Selection
        self.tableNameLabel = QtWidgets.QLabel("Table:")
        self.tableNameComboBox = QtWidgets.QComboBox(self)
        self.tableNameComboBox.addItems(tables.keys())

        self.chainNameLabel = QtWidgets.QLabel("Chain:")
        self.chainNameComboBox = QtWidgets.QComboBox(self)
        self.tableNameComboBox.currentIndexChanged.connect(self.updateChains)
        self.updateChains(0)  # Initialize chains for the first table

        # Decision for the whole rule
        self.decisionLabel = QtWidgets.QLabel("Decision:")
        self.decisionComboBox = QtWidgets.QComboBox(self)
        self.decisionComboBox.addItems(decisions)

        # Predicate Section
        self.predicateLayout = QtWidgets.QFormLayout()
        self.predicateWidgets = {}  # Store predicate widgets for easy access
        self.addPredicateButton = QtWidgets.QPushButton("Add Predicate")
        self.addPredicateButton.clicked.connect(self.addPredicate)

        # Button box
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Main layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.tableNameLabel)
        mainLayout.addWidget(self.tableNameComboBox)
        mainLayout.addWidget(self.chainNameLabel)
        mainLayout.addWidget(self.chainNameComboBox)
        mainLayout.addWidget(self.decisionLabel)
        mainLayout.addWidget(self.decisionComboBox)
        mainLayout.addLayout(self.predicateLayout)
        mainLayout.addWidget(self.addPredicateButton)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        # Connect signals
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def updateChains(self, index):
        """ Update chain names based on the selected table """
        table_name = self.tableNameComboBox.currentText()
        table = self.tables.get(table_name)
        self.chainNameComboBox.clear()
        if table:
            self.chainNameComboBox.addItems(table.getChains().keys())

    def addPredicate(self):
        """ Adds a new predicate input row with a ComboBox to select unused predicates """
        available_predicates = [f for f in self.fields if f not in self.used_predicates]
        if not available_predicates:
            QtWidgets.QMessageBox.information(self, "No More Predicates", "All predicates have been added.")
            return

        # Create a new predicate ComboBox
        predicateComboBox = QtWidgets.QComboBox(self)
        predicateComboBox.addItems(available_predicates)
        predicateComboBox.setEditable(False)

        # Predicate input field
        predicateInput = QtWidgets.QLineEdit(self)

        # Track widgets by predicate ComboBox reference
        self.predicateWidgets[predicateComboBox] = predicateInput

        # Add row to layout
        self.predicateLayout.addRow(predicateComboBox, predicateInput)
        self.used_predicates.add(predicateComboBox.currentText())  # Track used predicates

        # Update used predicates when ComboBox selection changes
        predicateComboBox.currentIndexChanged.connect(lambda: self.updateUsedPredicates(predicateComboBox))

    def updateUsedPredicates(self, comboBox):
        """ Update the list of available predicates when a ComboBox selection changes """
        self.used_predicates = {cb.currentText() for cb in self.predicateWidgets.keys()}
        available_predicates = [f for f in self.fields if f not in self.used_predicates]
        for cb in self.predicateWidgets.keys():
            current_selection = cb.currentText()
            cb.blockSignals(True)
            cb.clear()
            cb.addItems([current_selection] + available_predicates)
            cb.setCurrentText(current_selection)
            cb.blockSignals(False)

    def styleDialog(self):
        """ Apply a custom style sheet for the dialog """
        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QLabel {
                color: #dcdcdc;
            }
            QComboBox {
                background-color: #3a3a3a;  /* Darker background for ComboBox */
                color: #ffffff;              /* White text for better contrast */
                border: 1px solid #5a5a5a;
                padding: 5px;
            }
            QComboBox::drop-down {
                background-color: #3a3a3a;   /* Darker background for dropdown */
            }
            QComboBox QAbstractItemView {
                background-color: #3a3a3a;   /* Darker background for item view */
                color: #ffffff;               /* White text for better contrast */
            }
            QComboBox QAbstractItemView::item {
                padding: 5px;                 /* Add some padding for items */
            }
            QLineEdit, QSpinBox {
                border: 1px solid #5a5a5a;
                padding: 5px;
            }
            QPushButton {
                background-color: #4e4e4e;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)

    def getRuleDetails(self):
        """ Returns rule details as a dictionary for further processing """
        table_name = self.tableNameComboBox.currentText()
        chain_name = self.chainNameComboBox.currentText()
        decision = self.decisionComboBox.currentText()

        # Collect values from predicate fields
        predicates = {cb.currentText(): le.text() for cb, le in self.predicateWidgets.items()}
        
        return table_name, chain_name, decision, predicates

class StartupDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set the title and fixed size for the dialog
        self.setWindowTitle("Start Project")
        self.setFixedSize(600, 250)

        # Style the dialog for a modern look
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
                border-radius: 10px;
            }
            QLabel#titleLabel {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QLabel#subtitleLabel {
                font-size: 18px;
                color: #b3b3b3;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 16px;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
        """)

        # Left side: buttons for project options
        self.newProjectButton = QtWidgets.QPushButton("Create New Project")
        self.openProjectButton = QtWidgets.QPushButton("Open Project Folder")
        self.loadProjectButton = QtWidgets.QPushButton("Load Recent Project")
        
        # Layout for the buttons
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.addWidget(self.newProjectButton)
        buttonLayout.addWidget(self.openProjectButton)
        buttonLayout.addWidget(self.loadProjectButton)
        buttonLayout.setSpacing(20)

        # Right side: title label and image
        self.titleLabel = QtWidgets.QLabel("FWOptimizer")
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.subtitle = QtWidgets.QLabel("Firewall Optimization Tool")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        # Set margins to reduce spacing between title and subtitle
        self.titleLabel.setContentsMargins(0, 0, 15, 2)
        self.subtitle.setContentsMargins(0, 0, 15, 3)

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.imageLabel.setPixmap(QtGui.QPixmap(":/images/images/deku_tree_sprout.png").scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        # Layout for title, subtitle, and image
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.addWidget(self.titleLabel)
        rightLayout.addWidget(self.subtitle)
        rightLayout.addWidget(self.imageLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        rightLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        rightLayout.setSpacing(10)

        # Main layout
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(buttonLayout, 1)  # Left side
        mainLayout.addLayout(rightLayout, 1)   # Right side
        mainLayout.setContentsMargins(40, 40, 40, 40)

        self.setLayout(mainLayout)

        # Connect buttons to dialog actions
        self.newProjectButton.clicked.connect(lambda: self.done(1))
        self.openProjectButton.clicked.connect(lambda: self.done(2))
        self.loadProjectButton.clicked.connect(lambda: self.done(3))
