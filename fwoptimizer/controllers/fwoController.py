"""_summary_

Raises:
    IndexError: _description_

Returns:
    _type_: _description_
"""

from PyQt6.QtCore import pyqtSignal, QThread
import ctypes
import os

from model.fwoManager import FWOManager
from views.fwoView import FWOView
from model.consoleCommands import ConsoleCommands

class FWOController:
    """
    App Controller for user interaction
    """
    def __init__(self, model: FWOManager, view: FWOView):
        self.model: FWOManager = model
        self.view: FWOView = view
        self.console = ConsoleCommands(self.model, self.view, self.view.ui.console)
        
        self.workers = []
        
        self.connectSignals()
        
    def connectSignals(self):
        """
        Connect the view's and worker's signals with the model functions
        """
        view = self.view.ui
        model = self.model
        
        # Exit Confirmation
        view.actionExit.triggered.connect(self.closeConfirmation)
        self.view.closeEvent = self.closeConfirmation
        
        # Home button - Show WorkDir
        view.homeBtn.clicked.connect(
            lambda: (
                self.view.displayWorkingDirectoryTree(model.workFolder)
            )
        )
        view.treeWorkdirView.doubleClicked.connect(self.onTreeItemClicked)
        
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
    
    def closeConfirmation(self, event=None):
        """
        Ask for user confirmation to cancel tasks when trying to close
        the app.
        """
        if self.areTasksRunning():
            reply = self.view.showCloseConfirmationDialog('Confirmar Cierre',
            "Todavía hay tareas corriendo, cerrar la aplicación las cancelará.\nEstas seguro que deseas salir?")
            
            if reply is True:  # User clicked Yes
                self.cancelAllTasks()
                if event:
                    event.accept()
                else:
                    self.view.close()
            elif reply is False:  # User clicked No
                if event:
                    event.ignore()
            elif reply is None:  # User dismissed the dialog
                if event:
                    event.ignore()  # Ignore event and prevent closing
        else:
            reply = self.view.showCloseConfirmationDialog('Confirmar Cierre',
            "¿Quieres guardar antes de salir?")
            
            if reply is True:  # User clicked Yes
                if event:
                    self.saveProject()
                    event.accept()
                else:
                    self.view.close()
            elif reply is False:  # User clicked No
                if event:
                    self.view.close()
            elif reply is None:  # User canceled the dialog
                if event:
                    event.ignore()  # Ignore event and prevent closing
    
    def disableButtons(self):
        """
        Disable all functional Buttons
        """
        buttons = [
            self.view.ui.importBtn,
            self.view.ui.actionImport_Policy,
            self.view.ui.generateBtn,
            self.view.ui.viewBtn,
            self.view.ui.optimizeBtn,
            self.view.ui.exportBtn,
            self.view.ui.actionExport_Policy
        ]
        for button in buttons:
            button.setDisabled(True)

    def enableButtons(self):
        """
        Enable all functional Buttons
        """
        buttons = [
            self.view.ui.importBtn,
            self.view.ui.actionImport_Policy,
            self.view.ui.generateBtn,
            self.view.ui.viewBtn,
            self.view.ui.optimizeBtn,
            self.view.ui.exportBtn,
            self.view.ui.actionExport_Policy
        ]
        for button in buttons:
            button.setEnabled(True)
    
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
        
        # Get current firewall's Fields
        fields = self.model.currentFirewall.getFieldList().getFields()

        options = self.view.selectViewFddDialog(tables, fields)
        if options is None:
            return
        
        if options[0] == 'viewFDD':
            _ , (tableName, chainName), imageFrmt, graphDir, unrollDecisions = options
            print(f"Viewing FDD for {tableName} -> {chainName}:\n{imageFrmt} format, {graphDir} orientation, Unroll Decisions: {unrollDecisions}")
            self.runModelTask(self.model.viewFDD,
                            tableName,
                            chainName,
                            imageFrmt,
                            graphDir,
                            unrollDecisions
                            )
        elif options[0] == 'filterFDD':
            _ , tableName, chainName, field, match_expression, literal = options
            print(f"Filtering FDD for {tableName} -> {chainName}: {field} -> {match_expression}")
            self.runModelTask(self.model.filterFDD,
                              tableName,
                              chainName,
                              field,
                              match_expression,
                              literal
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

    def onTreeItemClicked(self, index):
        """
        Handle the event when a tree item is clicked.
        
        Args:
            index: The QModelIndex of the clicked item.
        """
        # Get the clicked item's data
        itemNode = self.view.ui.treeWorkdirView.model().itemFromIndex(index)

        # Get the detailsNode (second column), by getting the sibling in column 1
        detailsIndex = index.sibling(index.row(), 1)
        detailsNode = self.view.ui.treeWorkdirView.model().itemFromIndex(detailsIndex)

        # Retrieve the text from both the itemNode and the detailsNode
        itemText = itemNode.text()
        detailsText = detailsNode.text() if detailsNode else None

        # Define actions for specific file extensions
        fileActions = {
            '.txt': lambda path: self.view.displayReportsWindow(path),
            '.svg': lambda path: self.model.graphicsView.displayImage(f'{path}'),
            '.png': lambda path: self.model.graphicsView.displayImage(f'{path}'),
            '.jpg': lambda path: self.model.graphicsView.displayImage(f'{path}'),
        }

        # Or perform a more specific action, such as opening a file
        if "File" in detailsText:
            filePath = self.getFilePathFromItem(itemNode)  # Helper function to get the file path
            
            # Check for specific file extensions and perform the associated action
            for ext, action in fileActions.items():
                if itemText.endswith(ext):
                    action(filePath)  # Call the appropriate function
                    break  # Stop once the correct action is found

    def getFilePathFromItem(self, item):
        """
        Get the full file path from a tree item.
        
        Args:
            item: The QStandardItem representing a file.
        
        Returns:
            str: Full path to the file.
        """
        # Traverse up the tree to reconstruct the full file path
        parts = []
        while item:
            parts.insert(0, item.text())
            item = item.parent()
        return os.path.join(self.model.workFolder, *parts)

    def saveProject(self) -> None:
        """
        Select the file and save directory, then save the project to it.
        """
        filePath = self.view.saveProjectDialog()

        if filePath:
            self.model.saveProject(filePath)
            self.view.displayInfoMessage("Proyecto Guardado", "El proyecto se guardó exitosamente.")

    def loadProject(self) -> None:
        """
        Loads the project from the selected file.
        """
        filePath = self.view.selectFileDialog("FWO Files (*.fwo)")

        if filePath:
            self.model.loadProject(filePath)
            self.view.displayImportedRules(None, self.model.currentFirewall.getInputRules())
            
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
            self.disableButtons()
            self.console.executeCommand(command)
            self.enableButtons()

    """
                    THREADING
    """

    def runModelTask(self, func, *args, **kwargs):
        """
        Run a Model Task in its thread.

        Args:
            func : Function to run
        """
        worker = Worker(func, *args, **kwargs)
        worker.finished.connect(self.onTaskFinished)
        worker.error.connect(self.onTaskError)
        self.workers.append(worker)
        worker.start()
        self.view.showLoadingIndicator()
        
        # Get the function name
        funcName = func.__name__
        
        # Disable GUI buttons
        if funcName in ['importRules', 'generateFDD', 'viewFDD', 'optimizeFDD']:
            self.disableButtons()

    def onTaskFinished(self, task_name, result):
        """
        Handle the result on the view after finishing a Model's task

        Args:
            task_name: Task Executed
            result: Result obtained
        """
        self.view.showLoadingIndicator(False)
        # Handle the result based on the task name
        self.handleTaskResult(task_name, result)
        # Enable buttons
        self.enableButtons()
        # Clean Up Worker
        self.cleanupWorker()

    def onTaskError(self, task_name, error_message):
        """
        Handle the error from a task execution

        Args:
            task_name: Task Executed
            error_message: Error message to display
        """
        self.view.showLoadingIndicator(False)
        self.view.displayErrorMessage(f"Error in {task_name}: {error_message}")
        # Enable buttons
        self.enableButtons()
        # Clean Up Worker
        self.cleanupWorker()
        
    def handleTaskResult(self, task_name, result):
        """
        Handle each of the task results

        Args:
            task_name (function): Task executed
            result (obj): Result from task
        """
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
            
        elif task_name in ['viewFDD', 'filterFDD']:
            pathName, imgFormat = result
            if not pathName and task_name == 'filterFDD':
                self.view.displayInfoMessage("Filter FDD","No results for filter.")
                return
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
    
    def cleanupWorker(self):
        """
        Clean Up thread after it finishes its execution
        """
        if self.workers:
            worker = self.workers.pop(0)
            worker.quit()
            worker.wait()
            worker.deleteLater()
            
    def areTasksRunning(self):
        """
        Check wheter there are any tasks running in the background.

        Returns:
            bool: True if there are tasks running, False otherwise.
        """
        return any(worker.isRunning() for worker in self.workers)
            
    def cancelAllTasks(self):
        """
        Forcibly cancel all tasks running.
        """
        for worker in self.workers:
            if worker.isRunning():
                self.forceThreadTermination(worker)
            worker.quit()
            worker.wait()
            worker.deleteLater()
        self.workers.clear()
        self.view.showLoadingIndicator(False)
    
    def forceThreadTermination(self, thread):
        """
        Force a thread termination by rising a SystemExit Exception.

        Args:
            thread (QThread): Thread to terminate
        """
        thread_id = int(thread.currentThreadId())
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if res > 1: # If we get more than one Thread, cancel the exception, to avoid instability
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            print('Exception raise failure')
    
    def cleanUp(self):
        """
        Clean Up on close.
        """
        self.cancelAllTasks()

class Worker(QThread):
    """
    Worker Thread to execute long running tasks.

    """
    finished = pyqtSignal(str, object)
    error = pyqtSignal(str, str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
    
    def run(self):
        """
        Execute the task and pass the result to the main thread.
        """
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.error.emit(self.func.__name__, str(e))
        else:
            self.finished.emit(self.func.__name__, self.result)
