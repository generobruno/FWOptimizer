from PyQt6 import QtCore, QtGui, QtWidgets, QtSvg, QtSvgWidgets

class ImageViewer(QtWidgets.QGraphicsView):
    """
    ImageViewer Class

    Args:
        QtWidgets (_type_): _description_
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self.zoom_factor = 1.15  # Zoom in/out factor

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            super().wheelEvent(event)

    def zoomIn(self):
        self.scale(self.zoom_factor, self.zoom_factor)

    def zoomOut(self):
        self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.key() == QtCore.Qt.Key.Key_Plus:
                self.zoomIn()
            elif event.key() == QtCore.Qt.Key.Key_Minus:
                self.zoomOut()
        else:
            super().keyPressEvent(event)
            
    def displayImage(self, pathName):
        # Create a QGraphicsScene
        scene = QtWidgets.QGraphicsScene()
        
        if pathName.lower().endswith('.svg'):
            # For SVG files, use QGraphicsSvgItem
            svg_renderer = QtSvg.QSvgRenderer(pathName)
            svg_item = QtSvgWidgets.QGraphicsSvgItem()
            svg_item.setSharedRenderer(svg_renderer)
            scene.addItem(svg_item)
        else:
            # For raster images, use QPixmap
            pixmap = QtGui.QPixmap(pathName)
            if not pixmap.isNull():
                scene.addPixmap(pixmap)
            else:
                print("Failed to load the image.")
                return
            
        self.setStyleSheet(
        """
        #graphicsView, #graphFrame {
                background-color: white;
            }
        """
        )

        self.setScene(scene)
        self.fitInView(scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)