from PyQt6 import QtCore, QtGui, QtWidgets
from fwoptimizer.classes.firewall import Firewall
from fwoptimizer.classes import parser

class FWOManager:
    def __init__(self):
        # List of Firewalls Managed
        self.firewalls = []
        # Current Firewall
        self.currentFirewall = Firewall() #TODO CHANGE -> Guardar instancia de esto
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
            self.currentFirewall = self.firewalls[index]
        else:
            raise IndexError("Firewall index out of range.")

    def getActiveFirewall(self) -> Firewall:
        """
        Return the currently active firewall.
        """
        return self.currentFirewall
    
    def setParserStrategy(self, strategy):
        """
        Set the parser strategy.
        
        Args:
            strategy: Parser strategy to be used
        """
        self.parserStrategy = strategy
    
    def getParserStrategy(self):
        """
        Get the parser strategy

        Returns:
            strategy: Parser Strategy
        """
        return self.parserStrategy
    
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
    
    def _copyFile(self, filePath):
        """
        Copy file text

        Args:
            file_path (str): Path to file
        """
        with open(filePath, 'r') as file:
            data = file.read()
            return data

    def setFieldList(self):
        """
        Set the current Firewall's Field List
        """
        print("Setting Field List...")
        options = QtWidgets.QFileDialog.Option.ReadOnly
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=None,
            caption="Import Rules File",
            directory="",
            filter="Text Files (*.toml);;All Files (*)",
            options=options
        )

        if filePath:
            print(f"Setting FieldList from: {filePath}")
            self.currentFirewall.setFieldList(f'{filePath}')
            print("Field List set.")
            self.currentFirewall.getFieldList().printConfig()
        else:
            print("No file selected.")

    def generateFDD(self, table=None, chain=None):
        """
        Ask user for a FDD to generate from a chain

        Args:
            table (str, optional): Table Name. Defaults to None.
            chain (str, optional): Chain Name. Defaults to None.
        """
        print("Generating FDD...")
        if table is None and chain is None:
            self.currentFirewall.genFdd()
        else:
            self.currentFirewall.genFdd(table, chain)
            print(f'Printing out FDD')
            self.viewFDD(table, chain)
    
    def setGraphicsView(self, graphicsView):
        """
        Set the Graphics View

        Args:
            graphicsView (GraphicsView): Graphics View
        """
        self.graphicsView = graphicsView
    
    def viewFDD(self, table, chain, imgFormat='svg', graphDir='TB', unrollDecisions=False):
        """
        Display the FDD Graph in the graphicsView

        Args:
            table (str): Table Name
            chain (str): Chain Name
            imgFormat (str, optional): Output image format. Defaults to 'svg'.
            graphDir (str, optional): Graph Orientation. Defaults to 'TB'.
            unrollDecisions (bool, optional): Show explicit decisions. Defaults to False.
        """
        print(f"Displaying FDD for {table} - {chain}")
        
        # Generate graph
        fdd = self.currentFirewall.getFDD(chain)
        pathName = f'output/graphs/gen_{chain}'
        fdd.printFDD(pathName, img_format=imgFormat, rank_dir=graphDir, unroll_decisions=unrollDecisions)

        if self.graphicsView:
            # Create a QGraphicsScene
            scene = QtWidgets.QGraphicsScene()

            # Load the image as QPixmap
            pixmap = QtGui.QPixmap(pathName)

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
        
    def optimizeFDD(self, table=None, chain=None):
        """
        Ask user for a FDD to optimize

        Args:
            table (str, optional): Table Name. Defaults to None.
            chain (str, optional): Chain Name. Defaults to None.
        """
        print("Optimizing FDD...")
        if table is None and chain is None:
            self.currentFirewall.optimizeFdd()
        else:
            self.currentFirewall.optimizeFdd(table, chain)
            print(f'Printing out FDD')
            self.viewFDD(table, chain) #TODO Cambiar nombre para tener las 2 imagenes?
    
    def exportRules(self, table=None, chain=None):
        """
        Export RuleSet generated from an FDD.

        Args:
            table (str, optional): Table Name. Defaults to None.
            chain (str, optional): Chain Name. Defaults to None.

        Returns:
            RuleSet: Generated RuleSet
        """
        print("Exporting Rules...")
        if table is None and chain is None:
            return self.currentFirewall.genOutputRules()
        else:
            return self.currentFirewall.genOutputRules(table, chain)
        
        

        