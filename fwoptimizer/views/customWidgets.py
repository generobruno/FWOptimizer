"""_summary_
"""

from PyQt6 import QtCore, QtGui, QtWidgets

class ConsoleWidget(QtWidgets.QTextEdit):
    """
    Custom Console Widget 
    Emulates a console that interacts with the model

    Args:
        QtWidgets (QTextEdit): Text for the console
    """
    commandEntered = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setPlaceholderText("Type your command and press Enter...\nType 'help' to see available commands.")
        self.setFontFamily("Courier")
        self.setFontPointSize(10)
        self.command_history = []
        self.history_index = -1

        # Ensure the cursor is always at the end when starting
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextEditorInteraction)
        self.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    def keyPressEvent(self, event):
        # Ensure user can only type at the last line
        if self.textCursor().blockNumber() < self.document().blockCount() - 1:
            self.moveCursor(QtGui.QTextCursor.MoveOperation.End)

        if event.key() == QtCore.Qt.Key.Key_Return or event.key() == QtCore.Qt.Key.Key_Enter:
            command = self.toPlainText().splitlines()[-1].strip()
            self.commandEntered.emit(command)
            self.append("\n")  # Move to the next line after a command is entered
            self.command_history.append(command)
            self.history_index = len(self.command_history)
        elif event.key() == QtCore.Qt.Key.Key_Up:
            self.navigateCommandHistory(-1)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            self.navigateCommandHistory(1)
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        # Ensure the cursor is always at the end when clicking
        self.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        super().mousePressEvent(event)

    def navigateCommandHistory(self, direction):
        if not self.command_history:
            return

        self.history_index += direction
        self.history_index = max(0, min(self.history_index, len(self.command_history) - 1))
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(self.command_history[self.history_index])

    def appendToConsole(self, text):
        self.append(text)
        self.moveCursor(QtGui.QTextCursor.MoveOperation.End)
class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.setParent(parent)
        if edge == QtCore.Qt.Edge.LeftEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.Edge.TopEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.Edge.RightEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        elif edge == QtCore.Qt.Edge.BottomEdge:
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        widget = self.parentWidget()
        width = max(widget.minimumWidth(), widget.width() - delta.x())
        geo = widget.geometry()
        geo.setLeft(geo.right() - width)
        widget.setGeometry(geo)

    def resizeTop(self, delta):
        widget = self.parentWidget()
        height = max(widget.minimumHeight(), widget.height() - delta.y())
        geo = widget.geometry()
        geo.setTop(geo.bottom() - height)
        widget.setGeometry(geo)

    def resizeRight(self, delta):
        widget = self.parentWidget()
        width = max(widget.minimumWidth(), widget.width() + delta.x())
        widget.resize(width, widget.height())

    def resizeBottom(self, delta):
        widget = self.parentWidget()
        height = max(widget.minimumHeight(), widget.height() + delta.y())
        widget.resize(widget.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class ResizableWidget(QtWidgets.QWidget):
    _gripSize = 8
    def __init__(self, parent=None, resizable_edges=None):
        super().__init__(parent)

        # If no edges are specified, make all edges resizable by default
        if resizable_edges is None:
            resizable_edges = [
                QtCore.Qt.Edge.LeftEdge,
                QtCore.Qt.Edge.TopEdge,
                QtCore.Qt.Edge.RightEdge,
                QtCore.Qt.Edge.BottomEdge
            ]

        # Create side grips based on specified edges
        self.sideGrips = {}
        for edge in resizable_edges:
            self.sideGrips[edge] = SideGrip(self, edge)

        # Create corner grips only if adjacent edges are resizable
        self.cornerGrips = []
        if QtCore.Qt.Edge.LeftEdge in resizable_edges and QtCore.Qt.Edge.TopEdge in resizable_edges:
            self.cornerGrips.append(QtWidgets.QSizeGrip(self))
        if QtCore.Qt.Edge.TopEdge in resizable_edges and QtCore.Qt.Edge.RightEdge in resizable_edges:
            self.cornerGrips.append(QtWidgets.QSizeGrip(self))
        if QtCore.Qt.Edge.RightEdge in resizable_edges and QtCore.Qt.Edge.BottomEdge in resizable_edges:
            self.cornerGrips.append(QtWidgets.QSizeGrip(self))
        if QtCore.Qt.Edge.BottomEdge in resizable_edges and QtCore.Qt.Edge.LeftEdge in resizable_edges:
            self.cornerGrips.append(QtWidgets.QSizeGrip(self))

        self.updateGrips()

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)
        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # Position the corner grips
        if len(self.cornerGrips) >= 1:
            self.cornerGrips[0].setGeometry(QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        if len(self.cornerGrips) >= 2:
            self.cornerGrips[1].setGeometry(QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        if len(self.cornerGrips) >= 3:
            self.cornerGrips[2].setGeometry(QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        if len(self.cornerGrips) >= 4:
            self.cornerGrips[3].setGeometry(QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # Position the side grips
        if QtCore.Qt.Edge.LeftEdge in self.sideGrips:
            self.sideGrips[QtCore.Qt.Edge.LeftEdge].setGeometry(
                0, inRect.top(), self.gripSize, inRect.height())
        if QtCore.Qt.Edge.TopEdge in self.sideGrips:
            self.sideGrips[QtCore.Qt.Edge.TopEdge].setGeometry(
                inRect.left(), 0, inRect.width(), self.gripSize)
        if QtCore.Qt.Edge.RightEdge in self.sideGrips:
            self.sideGrips[QtCore.Qt.Edge.RightEdge].setGeometry(
                inRect.left() + inRect.width(), inRect.top(), self.gripSize, inRect.height())
        if QtCore.Qt.Edge.BottomEdge in self.sideGrips:
            self.sideGrips[QtCore.Qt.Edge.BottomEdge].setGeometry(
                self.gripSize, inRect.top() + inRect.height(), inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGrips()

class SlideMenu(QtWidgets.QWidget):
    """
    Custom SlideMenu Widget

    Args:
        QtWidgets (QWidget): Slide Menu
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftMenuContainer")
        
        # Set initial size
        self.collapsed_width = 50
        self.expanded_width = 100
        self.setFixedWidth(self.collapsed_width)
        
        self.is_expanded = False

    def toggle(self):
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.setFixedWidth(self.expanded_width)
        self.is_expanded = True
        self.updateButtonStyle()

    def collapse(self):
        self.setFixedWidth(self.collapsed_width)
        self.is_expanded = False
        self.updateButtonStyle()
        
    def updateButtonStyle(self):
        # Find the leftMenuSubContainer
        sub_container = self.findChild(QtWidgets.QWidget, "leftMenuSubContainer")
        if not sub_container:
            return

        # Find all frames in the sub_container
        frames = sub_container.findChildren(QtWidgets.QFrame)
        
        for frame in frames:
            
            layout = frame.layout()
            if layout:
                if self.is_expanded:
                    sub_container.setFixedWidth(100)
                    layout.setContentsMargins(0, 5, 0, 5)  # Restore margins when expanded
                    layout.setSpacing(0)
                    self.setStyleSheet("""
                        QWidget {
                            border-top-left-radius :8px;
                            border-top-right-radius : 0px;
                            border-bottom-left-radius : 8px;
                            border-bottom-right-radius : 8px;
                        }
                    """)
                else:
                    self.setFixedWidth(40)
                    layout.setContentsMargins(0, 5, 0, 5)  # Set margins to 0 when collapsed
                    layout.setSpacing(6)
                    self.setStyleSheet("""
                        QWidget {
                            border-top-left-radius :8px;
                            border-top-right-radius : 8px;
                            border-bottom-left-radius : 8px;
                            border-bottom-right-radius : 8px;
                        }
                    """)
                
            for button in frame.findChildren(QtWidgets.QPushButton):
                if self.is_expanded:
                    button.setStyleSheet("""
                        QPushButton {
                            border-radius: 8px;
                        }
                    """)
                    if hasattr(button, 'full_text'):
                        button.setText(button.full_text)
                else:
                    button.setStyleSheet("""
                        QPushButton {
                            text-align: left;
                            padding-left: 3px;
                            padding-right: 3px;
                        }
                    """)
                    if not hasattr(button, 'full_text'):
                        button.full_text = button.text()
                    button.setText("")