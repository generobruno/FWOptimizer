"""_summary_

Raises:
    IndexError: _description_

Returns:
    _type_: _description_
"""

import concurrent.futures
from PyQt6.QtCore import QObject, pyqtSignal

from model.fwoManager import FWOManager
from views.fwoView import FWOView
from model.consoleCommands import ConsoleCommands

# Maximum Number of workers to run the Model
MAX_WORKERS = 5

class FWOController:
    """
    App Controller for user interaction
    """
    def __init__(self, model: FWOManager, view: FWOView):
        self.model: FWOManager = model
        self.view: FWOView = view
        self.console = ConsoleCommands(self.model, self.view, self.view.ui.console)
        
        self.signals = WorkerSignals()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.futures = []
        
        self.connectSignals()
        
    def connectSignals(self):
        """
        Connect the view's and worker's signals with the model functions
        """
        view = self.view.ui
        model = self.model
        
        # Connect worker signals
        self.signals.finished.connect(self.onTaskFinished)
        self.signals.error.connect(self.onTaskError)
        
        # Connect buttons to model functions
        view.importBtn.clicked.connect(self.importRules)
        view.actionImport_Policy.triggered.connect(self.importRules)
        
        # Set FieldList Config
        view.actionSet_fieldList.triggered.connect(self.setFieldList)
        
        # Generate FDD Button
        view.generateBtn.clicked.connect(self.generateFDD)

        # Save Button
        view.actionSave_Project.triggered.connect(self.saveProject)
        # Load Button
        view.actionLoad_Project.triggered.connect(self.loadProject)
        
        # Pass the QGraphicsView reference to the model
        model.setGraphicsView(view.graphicsView)
        view.viewBtn.clicked.connect(self.viewFDD)
        
        # Optimize a FDD
        view.optimizeBtn.clicked.connect(self.optimizeFDD)
        
        # Generate and Export Rules optimized
        view.exportBtn.clicked.connect(self.exportRules)
        view.actionExport_Policy.triggered.connect(self.exportRules)
        
        # Connect the action to load parser syntax
        view.actionSet_parser.triggered.connect(self.setParserStrat)
        
        # Connect console commands
        view.console.commandEntered.connect(self.processCommand)
    
    def setParserStrat(self):
        """
        Select the parser Strategy
        """
        # TODO ask the user to choose a parser strategy, e.g., via a dialog
        #iptables_strat = parser.IpTablesParser()
        #parser_instance = parser.Parser(iptables_strat)
        #self.model.setParserStrategy(parser_instance)
        print("TODO: Parser strategy set.")
    
    def setFieldList(self):
        """
        Set the model's Field List
        """
        print("Setting Field List...")
        filePath = self.view.selectFileDialog("TOML Files (*.toml);;All Files (*)")
        
        if filePath:
            self.model.setFieldList(filePath)
        else:
            print("No file Selected.")
    
    def importRules(self):
        """
        Import Rules and save them in the Right Menu
        """
        filePath = self.view.selectFileDialog()
        
        if filePath:
            self.runModelTask(self.model.importRules, filePath)
        else:
            print("No file Selected.")
            
    def generateFDD(self):
        """
        Generate an FDD
        """
        if self.model.currentFirewall.getFieldList() is None:
            self.view.displayWarningMessage("No Field List loaded.\nPlease import it first.")
            return

        if not self.model.currentFirewall or not self.model.currentFirewall._inputRules:
            self.view.displayWarningMessage("No rules loaded.\nPlease import rules first.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall._inputRules.getTables()

        # User selects option to generate
        option = self.view.selectFddDialog(tables)
        
        # Generate FDD given user selection
        if option == "all":  
            self.runModelTask(self.model.generateFDD)
        elif isinstance(option, tuple):
            tableName, chainName = option
            self.runModelTask(self.model.generateFDD, tableName, chainName)
        else:
            self.view.displayWarningMessage("No valid option selected for FDD generation.")
            
    def viewFDD(self):
        """
        Display the FDD
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayWarningMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return

        # Get all tables from the current firewall's RuleSet
        tables = self.model.currentFirewall.getInputRules().getTables()

        options = self.view.selectViewFddDialog(tables)
        
        if options:
            (tableName, chainName), imageFrmt, graphDir, unrollDecisions = options
            print(f"Viewing FDD for {tableName} -> {chainName}:\n{imageFrmt} format, {graphDir} orientation, Unroll Decisions: {unrollDecisions}")
            self.runModelTask(self.model.viewFDD,
                            tableName,
                            chainName,
                            imageFrmt,
                            graphDir,
                            unrollDecisions
                            )
            
    def optimizeFDD(self):
        """
        Optimize the FDD
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayWarningMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.getInputRules().getTables()

        # User selects option to generate
        option = self.view.selectFddDialog(tables)
        
        # Optimize FDD given user selection
        if option == "all":  
            self.runModelTask(self.model.optimizeFDD)
        elif isinstance(option, tuple):
            tableName, chainName = option
            self.runModelTask(self.model.optimizeFDD, tableName, chainName)
        else:
            self.view.displayWarningMessage("No valid option selected for FDD generation.")
            
    def exportRules(self):
        """
        Generate Rules and Export them to a file
        """
        if not self.model.currentFirewall or len(self.model.currentFirewall.getFDDs()) == 0:
            self.view.displayWarningMessage("No FDD Generated.\nPlease generate an FDD for the firewall.")
            return
        
        # Get all tables
        tables = self.model.currentFirewall.getInputRules().getTables()

        # User selects option and file path
        option, filePath = self.view.exportRulesDialog(tables)
        
        if option and filePath:
            # Generate rules given user selection
            if option == "all":
                exportedRules = self.model.exportRules()
            elif isinstance(option, tuple):
                tableName, chainName = option
                print(f'Exporting specific - Table: {tableName}, Chain: {chainName}')
                exportedRules = self.model.exportRules(tableName, chainName)
            else:
                self.view.displayWarningMessage("No valid option selected for FDD generation.")
                return
            
            # Generate export File from RuleSet, given the Parser Strategy
            fileContent = self.model.getParserStrategy().compose(exportedRules)
            
            # Save exported rules to right menu 
            if fileContent:
                self.view.displayExportedRules(fileContent)
                
                # Write the file content to the specified file path
                with open(filePath, 'w') as file:
                    file.write(fileContent)
                
                print(f'Exported file to: {filePath}')
        else:
            self.view.displayWarningMessage("No valid option or file path selected for export.")

    def saveProject(self) -> None:
        """
        Select the file and save directory, then save the project to it.
        
        """

        filePath = self.view.saveProjectDialog()

        if filePath:

            self.model.saveProject(filePath)

    def loadProject(self) -> None:
        """
        Loads the project from the selected file.
        
        """

        filePath = self.view.selectFileDialog()

        if filePath:

            self.model.loadProject(filePath)
            
    def processCommand(self, command):
        """
        Process a command entered in the console.

        Args:
            command (str): Command entered by the user
        """
        if command == 'exit':
            self.view.ui.consoleContainer.hide()
            self.view.ui.console.clear()
        else:
            self.console.executeCommand(command)
        
    def taskWrapper(self, func, *args, **kwargs):
        """
        Wrap a Model's function to be executed by a worker.

        Args:
            func (obj): Model's function.
        """
        try:
            result = func(*args, **kwargs)
            self.signals.finished.emit(func.__name__, result)
        except Exception as e:
            self.signals.error.emit(func.__name__, str(e))
        
    def runModelTask(self, func, *args, **kwargs):
        """
        Run a Model Task in its thread.

        Args:
            func : Function to run
        """
        future = self.executor.submit(self.taskWrapper, func, *args, **kwargs)
        self.futures.append(future)
        self.view.showLoadingIndicator()
        
        # Get the function name
        funcName = func.__name__
        
        # Disable GUI buttons
        if funcName in ['importRules', 'generateFDD', 'viewFDD', 'optimizeFDD']:
            self.view.ui.importBtn.setDisabled(True)
            self.view.ui.actionImport_Policy.setDisabled(True)
            self.view.ui.generateBtn.setDisabled(True)
            self.view.ui.viewBtn.setDisabled(True)
            self.view.ui.optimizeBtn.setDisabled(True)
            self.view.ui.exportBtn.setDisabled(True)
            self.view.ui.actionExport_Policy.setDisabled(True)

    def onTaskFinished(self, task_name, result):
        """
        Handle the result on the view after finishing a Model's task

        Args:
            task_name: Task Executed
            result: Result obtained
        """
        self.view.showLoadingIndicator(False)
        # Handle the result based on the task name
        if task_name == 'importRules':
            self.view.displayImportedRules(result[0], result[1])
        elif task_name == 'generateFDD':
            tableName, chainName = result
            if tableName is not None and chainName is not None:
                    pathName, imgFormat = self.model.viewFDD(tableName, chainName)
                    if self.model.graphicsView:
                        self.model.graphicsView.displayImage(f'{pathName}.{imgFormat}')
                    else:
                        self.view.displayErrorMessage("Image Display not set.")
            # Enable Buttons
            self.view.ui.generateBtn.setEnabled(True)
        elif task_name == 'viewFDD':
            pathName, imgFormat = result
            if self.model.graphicsView:
                self.model.graphicsView.displayImage(f'{pathName}.{imgFormat}')
            else:
                self.view.displayErrorMessage("Image Display not set.")
        elif task_name == 'optimizeFDD':
            tableName, chainName = result
            if tableName is not None and chainName is not None:
                    pathName, imgFormat = self.model.viewFDD(tableName, chainName)
                    if self.model.graphicsView:
                        self.model.graphicsView.displayImage(f'{pathName}.{imgFormat}')
                    else:
                        self.view.displayErrorMessage("Image Display not set.")
           
        # Enable buttons
        self.view.ui.importBtn.setEnabled(True)
        self.view.ui.actionImport_Policy.setEnabled(True)             
        self.view.ui.generateBtn.setEnabled(True)
        self.view.ui.viewBtn.setEnabled(True)
        self.view.ui.optimizeBtn.setEnabled(True)
        self.view.ui.exportBtn.setEnabled(True)
        self.view.ui.actionExport_Policy.setEnabled(True)

    def onTaskError(self, task_name, error_message):
        """
        Handle the error from a task execution

        Args:
            task_name: Task Executed
            error_message: Error message to display
        """
        self.view.showLoadingIndicator(False)
        self.view.displayErrorMessage(f"Error in {task_name}: {error_message}")
        
    def cleanUp(self):
        """
        Gracefully stop the app.
        """
        # Shutdown the executor and cancel any pending futures
        self.executor.shutdown(wait=False, cancel_futures=True)

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc())
    '''
    finished = pyqtSignal(str, object)
    error = pyqtSignal(str, str)
