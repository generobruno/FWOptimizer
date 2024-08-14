from PyQt6 import QtCore, QtGui, QtWidgets

class ConsoleWidget(QtWidgets.QTextEdit):
    # Signal to emit the command text
    commandEntered = QtCore.pyqtSignal(str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setPlaceholderText("Type your command and press Enter...\nType 'help' to see available commands.")
        self.setFontFamily("Courier")
        self.setFontPointSize(10)
        self.command_history = []
        self.history_index = -1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return or event.key() == QtCore.Qt.Key.Key_Enter:
            command = self.toPlainText().splitlines()[-1]
            self.commandEntered.emit(command)
            self.append("\n")  # Move to the next line after a command is entered
        elif event.key() == QtCore.Qt.Key.Key_Up:
            self.navigateCommandHistory(-1)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            self.navigateCommandHistory(1)
        else:
            super().keyPressEvent(event)

    def navigateCommandHistory(self, direction):
        if not self.command_history:
            return

        self.history_index += direction
        self.history_index = max(0, min(self.history_index, len(self.command_history) - 1))
        self.textCursor().select(QtGui.QTextCursor.SelectionType.LineUnderCursor)
        self.textCursor().removeSelectedText()
        self.append(self.command_history[self.history_index])

    def appendToConsole(self, text):
        self.append(text)

class SlideMenu(QtWidgets.QWidget):
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