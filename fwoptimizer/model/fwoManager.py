from PyQt6 import QtCore, QtGui, QtWidgets

class FWOManager:
    def __init__(self):
        self.graphicsView = None
    
    def importRules(self):
        """
        Import a file with rules
        """
        print("Importing Rules.")
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
            return self._processFile(file_path)
        else:
            print("No file selected.")
            return None
        
    def _processFile(self, file_path):
        # Implement your file processing logic here
        with open(file_path, 'r') as file:
            data = file.read()
            print(f"File content: {data}")
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