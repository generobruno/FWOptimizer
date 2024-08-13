from PyQt6 import QtWidgets

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