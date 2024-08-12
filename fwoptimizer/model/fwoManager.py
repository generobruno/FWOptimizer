from PyQt6 import QtCore, QtGui, QtWidgets
from fwoptimizer.classes.firewall import Firewall
from fwoptimizer.classes import parser

class FWOManager:
    def __init__(self):
        # List of Firewalls Managed
        self.firewalls = []
        # Current Firewall
        self.currentFirewall = Firewall() #TODO CHANGE
        # Current Parser Strategy (Default to IpTables)
        self.parserStrategy = parser.IpTablesParser()
        # Graphics Viewer
        self.graphicsView = None
        
    def addFirewall(self, firewall: Firewall):
        """
        Add a new Firewall to the manager.
        """
        self.firewalls.append(firewall)
        self.setActiveFirewall(len(self.firewalls) - 1)

    def setActiveFirewall(self, index: int):
        """
        Set the active firewall by its index in the firewalls list.
        """
        if 0 <= index < len(self.firewalls):
            self.current_firewall = self.firewalls[index]
        else:
            raise IndexError("Firewall index out of range.")

    def getActiveFirewall(self) -> Firewall:
        """
        Return the currently active firewall.
        """
        return self.current_firewall
    
    def setParserStrategy(self, strategy):
        """
        Set the parser strategy.
        
        Args:
            strategy: Parser strategy to be used
        """
        self.parserStrategy = strategy
    
    def importRules(self):
        """
        Import Rules from a file

        Returns:
            str: Rules in file as text
            RuleSet: RuleSet extracted from file
        """
        if self.parserStrategy is None:
            print("No parser strategy set.")
            return None, None
        
        print("Importing Rules...")
        options = QtWidgets.QFileDialog.Option.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=None,
            caption="Import Rules File",
            directory="",
            filter="All Files (*);;Text Files (*.txt);;XML Files (*.xml)",
            options=options
        )

        if file_path:
            print(f"Importing Rules from: {file_path}")
            rulesParsed = self.parserStrategy.parse(file_path)
            if self.currentFirewall:
                self.currentFirewall.inputRules = rulesParsed
                print("Rules parsed and saved to the current firewall.")
                return self._copyFile(file_path), rulesParsed
            else:
                print("No firewall selected to save the parsed rules.")
                return None, None
        else:
            print("No file selected.")
            return None, None
    
    def _copyFile(self, file_path):
        """
        Copy file text

        Args:
            file_path (str): Path to file
        """
        with open(file_path, 'r') as file:
            data = file.read()
            return data

    def generateFDD(self):
        print("Generating FDD...")
        
    def viewFDD(self):
        print("Displaying FDD...")

        if self.graphicsView:
            # Create a QGraphicsScene
            scene = QtWidgets.QGraphicsScene()

            # Load the image as QPixmap
            pixmap = QtGui.QPixmap("resources\images\deku_tree_sprout.png")  # Replace with your image path

            if not pixmap.isNull():
                # Add the QPixmap to the scene as a QGraphicsPixmapItem
                scene.addPixmap(pixmap)

                # Set the scene to the graphicsView
                self.graphicsView.setScene(scene)

                # Center the image in the view
                self.graphicsView.fitInView(scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            else:
                print("Failed to load the image.")
        else:
            print("Graphics view is not set.")
        
    def optimizeFDD(self):
        print("Optimizing...")
    
    def exportRules(self):
        print("Exporting Rules...")
        
    def setGraphicsView(self, graphics_view):
        self.graphicsView = graphics_view