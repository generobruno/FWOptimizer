"""_summary_

Raises:
    IndexError: _description_

Returns:
    _type_: _description_
"""

import pickle
import zipfile
import os
from fwoptimizer.classes.firewall import Firewall
from fwoptimizer.classes import parser

class FWOManager:
    """
    Top Module of the App Model
    """
    def __init__(self, workFolder = "workdir/"):
        # Work folder
        self.workFolder = workFolder
        if not os.path.exists(self.workFolder):
            os.makedirs(self.workFolder)
        # List of Firewalls Managed
        self.firewalls = []
        # Current Firewall
        self.currentFirewall = Firewall(workFolder=self.workFolder)
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
    
    def importRules(self, filePath):
        """
        Import Rules from a file

        Returns:
            str: Rules in file as text
            RuleSet: RuleSet extracted from file
        """
        if self.parserStrategy is None:
            print("No parser strategy set.")
            return None, None

        print(f"Importing Rules from: {filePath}")
        rulesParsed = self.parserStrategy.parse(filePath)
        if self.currentFirewall:
            self.currentFirewall.setInputRules(rulesParsed)
            print("Rules parsed and saved to the current firewall.")
            return self._copyFile(filePath), rulesParsed
        else:
            print("No firewall selected to save the parsed rules.")
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

    def setFieldList(self, filePath):
        """
        Set the current Firewall's Field List
        """
        print(f"Setting FieldList from: {filePath}")
        self.currentFirewall.setFieldList(f'{filePath}')
        print("Field List set.")
        self.currentFirewall.getFieldList().printConfig()

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
        pathName = self.workFolder + f'graphs/gen_{chain}'
        fdd.printFDD(pathName, img_format=imgFormat, rank_dir=graphDir, unroll_decisions=unrollDecisions)

        if self.graphicsView:
            self.graphicsView.displayImage(f'{pathName}.{imgFormat}')
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
        
    def saveProject(self, filePath):
        
        serializedFirewallPath = self.workFolder + "firewall.pkl"

        # Serialize firewall object
        with open(serializedFirewallPath, 'wb') as file:
            pickle.dump(self.currentFirewall, file)

        # Createa ZIP File in save_path
        with zipfile.ZipFile(filePath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Recorrer el directorio output/
            for root, dirs, files in os.walk(self.workFolder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Agregar el archivo al ZIP, manteniendo la estructura de directorios
                    zipf.write(file_path, os.path.relpath(file_path, self.workFolder))

        #Remove serialized object
        if os.path.exists(serializedFirewallPath):
            os.remove(serializedFirewallPath)

    def loadProject(self, filePath):

        serializedFirewallPath = self.workFolder + "firewall.pkl"

        def removeDir(dirPath):
            for filename in os.listdir(dirPath):
                path = os.path.join(dirPath, filename)
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        removeDir(path)
                        os.rmdir(path)
                except Exception as e:
                    print(f'Error al eliminar {path}: {e}')

        # Eliminar todo el contenido del directorio de trabajo
        removeDir(self.workFolder)

        # Extraer el archivo en el directorio de trabajo
        with zipfile.ZipFile(filePath, 'r') as zip_ref:
            zip_ref.extractall(self.workFolder)

        # Deserializar el firewall
        with open(serializedFirewallPath, 'rb') as file:
            self.currentFirewall = pickle.load(file)

        # Borrar el archivo de serializado
        if os.path.exists(serializedFirewallPath):
            os.remove(serializedFirewallPath)



        