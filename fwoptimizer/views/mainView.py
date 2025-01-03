from PyQt6 import QtCore, QtGui, QtWidgets
from views.imageView import ImageViewer
from views.customWidgets import SlideMenu, ConsoleWidget, ResizableWidget, Spinner
import fwoptimizer.views.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1054, 685)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/deku_tree_sprout.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("* {\n"
"    border: none;\n"
"    background-color:transparent;\n"
"    background: transparent;\n"
"    padding:0;\n"
"    margin:0;\n"
"    color: #fff;\n"
"}\n"
"QMenuBar, QMenu, QStatusBar, QAction {\n"
"    background-color: #1f232a;\n"
"}\n"
"#centralWidget {\n"
"    background-color: #1f232a;\n"
"}\n"
"#leftMenuSubContainer {\n"
"    background-color: #16191d;\n"
"    border-radius: 8px;\n"
"    border-top-right-radius: 0px;\n"
"}\n"
"#leftMenuSubContainer QPushButton {\n"
"    text-align: left;\n"
"    padding: 2px 5px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"}\n"
"#centerMenuSubContainer, #rightMenuSubContainer {\n"
"    background-color: #2c313c;\n"
"    border-radius: 8px;\n"
"}\n"
"#rightMenuFrame, #popupNotificationSubContainer {\n"
"    background-color: #16191d;\n"
"    border-radius: 8px;\n"
"}\n"
"#centerMenuFrame {\n"
"    background-color: #16191d;\n"
"    border-top-left-radius :0px;\n"
"    border-top-right-radius : 8px; \n"
"    border-bottom-left-radius : 0px; \n"
"    border-bottom-right-radius : 8px\n"
"}\n"
"#headerContainer, #footerContainer {\n"
"    background-color: #2c313c;\n"
"    border-radius: 8px;\n"
"}\n"
"#graphicsView, #graphFrame {\n"
"    border-radius: 8px;\n"
"}\n"
"#consoleWidget {\n"
"    background-color: #16191d;\n"
"    border-radius: 8px;\n"
"}")
        self.centralWidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # Custom SlideMenu Widget
        self.leftMenuContainer = SlideMenu(parent=self.centralWidget)
        self.leftMenuContainer.setMaximumSize(QtCore.QSize(200, 16777215))
        self.leftMenuContainer.setObjectName("leftMenuContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.leftMenuContainer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leftMenuSubContainer = QtWidgets.QWidget(parent=self.leftMenuContainer)
        self.leftMenuSubContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.leftMenuSubContainer.setObjectName("leftMenuSubContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.leftMenuTopFrame = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        self.leftMenuTopFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftMenuTopFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftMenuTopFrame.setObjectName("leftMenuTopFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.leftMenuTopFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.leftMenuBtn = QtWidgets.QPushButton(parent=self.leftMenuTopFrame)
        self.leftMenuBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/align-justify.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.leftMenuBtn.setIcon(icon1)
        self.leftMenuBtn.setIconSize(QtCore.QSize(24, 24))
        self.leftMenuBtn.setObjectName("leftMenuBtn")
        self.verticalLayout_3.addWidget(self.leftMenuBtn)
        self.verticalLayout_2.addWidget(self.leftMenuTopFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.leftMenuUpFrame = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuUpFrame.sizePolicy().hasHeightForWidth())
        self.leftMenuUpFrame.setSizePolicy(sizePolicy)
        self.leftMenuUpFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftMenuUpFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftMenuUpFrame.setObjectName("leftMenuUpFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.leftMenuUpFrame)
        self.verticalLayout_4.setContentsMargins(0, 5, 0, 5)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.homeBtn = QtWidgets.QPushButton(parent=self.leftMenuUpFrame)
        self.homeBtn.setStyleSheet("background-color: #1f232a;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/home.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.homeBtn.setIcon(icon2)
        self.homeBtn.setIconSize(QtCore.QSize(24, 24))
        self.homeBtn.setObjectName("homeBtn")
        self.verticalLayout_4.addWidget(self.homeBtn)
        self.rulesBtn = QtWidgets.QPushButton(parent=self.leftMenuUpFrame)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/list.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.rulesBtn.setIcon(icon3)
        self.rulesBtn.setIconSize(QtCore.QSize(24, 24))
        self.rulesBtn.setObjectName("rulesBtn")
        self.verticalLayout_4.addWidget(self.rulesBtn)
        self.consoleBtn = QtWidgets.QPushButton(parent=self.leftMenuUpFrame)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/terminal.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.consoleBtn.setIcon(icon4)
        self.consoleBtn.setIconSize(QtCore.QSize(24, 24))
        self.consoleBtn.setObjectName("consoleBtn")
        self.verticalLayout_4.addWidget(self.consoleBtn)
        self.verticalLayout_2.addWidget(self.leftMenuUpFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.leftMenuBottomFrame = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        self.leftMenuBottomFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftMenuBottomFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftMenuBottomFrame.setObjectName("leftMenuBottomFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.leftMenuBottomFrame)
        self.verticalLayout_5.setContentsMargins(0, 5, 0, 5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.reportsBtn = QtWidgets.QPushButton(parent=self.leftMenuBottomFrame)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/printer.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.reportsBtn.setIcon(icon5)
        self.reportsBtn.setIconSize(QtCore.QSize(24, 24))
        self.reportsBtn.setObjectName("reportsBtn")
        self.verticalLayout_5.addWidget(self.reportsBtn)
        self.settingsBtn = QtWidgets.QPushButton(parent=self.leftMenuBottomFrame)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/settings.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.settingsBtn.setIcon(icon6)
        self.settingsBtn.setIconSize(QtCore.QSize(24, 24))
        self.settingsBtn.setObjectName("settingsBtn")
        self.verticalLayout_5.addWidget(self.settingsBtn)
        self.helpBtn = QtWidgets.QPushButton(parent=self.leftMenuBottomFrame)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/help-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.helpBtn.setIcon(icon7)
        self.helpBtn.setIconSize(QtCore.QSize(24, 24))
        self.helpBtn.setObjectName("helpBtn")
        self.verticalLayout_5.addWidget(self.helpBtn)
        self.verticalLayout_2.addWidget(self.leftMenuBottomFrame, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.verticalLayout.addWidget(self.leftMenuSubContainer)
        self.horizontalLayout.addWidget(self.leftMenuContainer)
        # Resizable Widget
        self.centerMenuContainer = ResizableWidget(self.centralWidget, resizable_edges=[
            QtCore.Qt.Edge.RightEdge
        ])
        self.centerMenuContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.centerMenuContainer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centerMenuContainer.setObjectName("centerMenuContainer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centerMenuContainer)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6") 
        self.centerMenuSubContainer = QtWidgets.QWidget(parent=self.centerMenuContainer)
        self.centerMenuSubContainer.setMinimumSize(QtCore.QSize(200, 0))
        self.centerMenuSubContainer.setObjectName("centerMenuSubContainer")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centerMenuSubContainer)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.centerMenuFrame = QtWidgets.QFrame(parent=self.centerMenuSubContainer)
        self.centerMenuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.centerMenuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.centerMenuFrame.setObjectName("centerMenuFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centerMenuFrame)
        self.horizontalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.centerMenuFrame)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.closeCenterMenuBtn = QtWidgets.QPushButton(parent=self.centerMenuFrame)
        self.closeCenterMenuBtn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/x-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.closeCenterMenuBtn.setIcon(icon8)
        self.closeCenterMenuBtn.setIconSize(QtCore.QSize(20, 20))
        self.closeCenterMenuBtn.setObjectName("closeCenterMenuBtn")
        self.horizontalLayout_2.addWidget(self.closeCenterMenuBtn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_7.addWidget(self.centerMenuFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.centerMenuStack = QtWidgets.QStackedWidget(parent=self.centerMenuSubContainer)
        self.centerMenuStack.setStyleSheet("")
        self.centerMenuStack.setObjectName("centerMenuStack")
        self.settingsPage = QtWidgets.QWidget()
        self.settingsPage.setObjectName("settingsPage")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.settingsPage)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_2 = QtWidgets.QLabel(parent=self.settingsPage)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_8.addWidget(self.label_2)
        self.centerMenuStack.addWidget(self.settingsPage)
        self.policiesPage = QtWidgets.QWidget()
        self.policiesPage.setObjectName("policiesPage")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.policiesPage)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.treePoliciesView = QtWidgets.QTreeView(parent=self.policiesPage)
        self.treePoliciesView.setObjectName("treePoliciesView")
        self.verticalLayout_9.addWidget(self.treePoliciesView)
        self.centerMenuStack.addWidget(self.policiesPage)
        
        # Home Page
        self.HomePage = QtWidgets.QWidget()
        self.HomePage.setObjectName(u"HomePage")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.HomePage)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.treeWorkdirView = QtWidgets.QTreeView(self.HomePage)
        self.treeWorkdirView.setObjectName(u"treeWorkdirView")
        self.verticalLayout_18.addWidget(self.treeWorkdirView)
        self.centerMenuStack.addWidget(self.HomePage)
        
        self.helpPage = QtWidgets.QWidget()
        self.helpPage.setObjectName("helpPage")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.helpPage)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(parent=self.helpPage)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.centerMenuStack.addWidget(self.helpPage)
        self.verticalLayout_7.addWidget(self.centerMenuStack)
        self.verticalLayout_6.addWidget(self.centerMenuSubContainer)
        self.horizontalLayout.addWidget(self.centerMenuContainer)
        self.mainBodyContainer = QtWidgets.QWidget(parent=self.centralWidget)
        self.mainBodyContainer.setMinimumSize(QtCore.QSize(400, 0))
        self.mainBodyContainer.setStyleSheet("")
        self.mainBodyContainer.setObjectName("mainBodyContainer")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.mainBodyContainer)
        self.verticalLayout_11.setContentsMargins(3, 3, 0, 0)
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.headerContainer = QtWidgets.QWidget(parent=self.mainBodyContainer)
        self.headerContainer.setObjectName("headerContainer")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.headerContainer)
        self.horizontalLayout_4.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.leftHeaderFrame = QtWidgets.QFrame(parent=self.headerContainer)
        self.leftHeaderFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.leftHeaderFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.leftHeaderFrame.setObjectName("leftHeaderFrame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.leftHeaderFrame)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.logo = QtWidgets.QLabel(parent=self.leftHeaderFrame)
        self.logo.setMaximumSize(QtCore.QSize(30, 30))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/images/images/deku_tree_sprout.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout_6.addWidget(self.logo)
        self.title = QtWidgets.QLabel(parent=self.leftHeaderFrame)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setToolTip("")
        self.title.setObjectName("title")
        self.horizontalLayout_6.addWidget(self.title)
        # Loading Spinner
        self.loading = Spinner(parent=self.leftHeaderFrame)
        self.loading.setObjectName("loading")
        self.horizontalLayout_6.addWidget(self.loading)
        self.horizontalLayout_4.addWidget(self.leftHeaderFrame, 0, QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.rightHeaderFrame = QtWidgets.QFrame(parent=self.headerContainer)
        self.rightHeaderFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.rightHeaderFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.rightHeaderFrame.setObjectName("rightHeaderFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.rightHeaderFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.importBtn = QtWidgets.QPushButton(parent=self.rightHeaderFrame)
        self.importBtn.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/upload.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.importBtn.setIcon(icon9)
        self.importBtn.setObjectName("importBtn")
        self.horizontalLayout_3.addWidget(self.importBtn)
        self.generateBtn = QtWidgets.QPushButton(parent=self.rightHeaderFrame)
        self.generateBtn.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.generateBtn.setIcon(icon10)
        self.generateBtn.setObjectName("generateBtn")
        self.horizontalLayout_3.addWidget(self.generateBtn)
        self.optimizeBtn = QtWidgets.QPushButton(parent=self.rightHeaderFrame)
        self.optimizeBtn.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/tool.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.optimizeBtn.setIcon(icon11)
        self.optimizeBtn.setIconSize(QtCore.QSize(16, 16))
        self.optimizeBtn.setObjectName("optimizeBtn")
        self.horizontalLayout_3.addWidget(self.optimizeBtn)
        self.viewBtn = QtWidgets.QPushButton(parent=self.rightHeaderFrame)
        self.viewBtn.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/icons/eye.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.viewBtn.setIcon(icon12)
        self.viewBtn.setObjectName("viewBtn")
        self.horizontalLayout_3.addWidget(self.viewBtn)
        self.exportBtn = QtWidgets.QPushButton(parent=self.rightHeaderFrame)
        self.exportBtn.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/icons/download.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.exportBtn.setIcon(icon13)
        self.exportBtn.setObjectName("exportBtn")
        self.horizontalLayout_3.addWidget(self.exportBtn)
        self.horizontalLayout_4.addWidget(self.rightHeaderFrame, 0, QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_11.addWidget(self.headerContainer, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainBodyContent = QtWidgets.QWidget(parent=self.mainBodyContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBodyContent.sizePolicy().hasHeightForWidth())
        self.mainBodyContent.setSizePolicy(sizePolicy)
        self.mainBodyContent.setObjectName("mainBodyContent")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.mainBodyContent)
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.mainContentsContainer = QtWidgets.QWidget(parent=self.mainBodyContent)
        self.mainContentsContainer.setObjectName("mainContentsContainer")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.mainContentsContainer)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.graphFrame = QtWidgets.QFrame(parent=self.mainContentsContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphFrame.sizePolicy().hasHeightForWidth())
        self.graphFrame.setSizePolicy(sizePolicy)
        self.graphFrame.setMinimumSize(QtCore.QSize(400, 400))
        self.graphFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.graphFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.graphFrame.setObjectName("graphFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.graphFrame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        #self.graphicsView = QtWidgets.QGraphicsView(parent=self.graphFrame)
        self.graphicsView = ImageViewer(parent=self.graphFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(400, 400))
        self.graphicsView.setStyleSheet("")
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_5.addWidget(self.graphicsView)
        self.verticalLayout_16.addWidget(self.graphFrame)
        self.horizontalLayout_7.addWidget(self.mainContentsContainer)
        #self.rightMenuContainer = QtWidgets.QWidget(parent=self.mainBodyContent)
        self.rightMenuContainer = ResizableWidget(parent=self.mainBodyContent, resizable_edges=[
            QtCore.Qt.Edge.LeftEdge
        ])
        self.rightMenuContainer.setMinimumSize(QtCore.QSize(300, 0))
        self.rightMenuContainer.setObjectName("rightMenuContainer")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.rightMenuContainer)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.rightMenuSubContainer = QtWidgets.QWidget(parent=self.rightMenuContainer)
        self.rightMenuSubContainer.setObjectName("rightMenuSubContainer")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.rightMenuSubContainer)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.rightMenuFrame = QtWidgets.QFrame(parent=self.rightMenuSubContainer)
        self.rightMenuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.rightMenuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.rightMenuFrame.setObjectName("rightMenuFrame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.rightMenuFrame)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel(parent=self.rightMenuFrame)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.closeRightMenuBtn = QtWidgets.QPushButton(parent=self.rightMenuFrame)
        self.closeRightMenuBtn.setText("")
        self.closeRightMenuBtn.setIcon(icon8)
        self.closeRightMenuBtn.setIconSize(QtCore.QSize(20, 20))
        self.closeRightMenuBtn.setObjectName("closeRightMenuBtn")
        self.horizontalLayout_8.addWidget(self.closeRightMenuBtn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_13.addWidget(self.rightMenuFrame)
        self.rightMenuStack = QtWidgets.QStackedWidget(parent=self.rightMenuSubContainer)
        self.rightMenuStack.setObjectName("rightMenuStack")
        self.exportedPage = QtWidgets.QWidget()
        self.exportedPage.setObjectName("exportedPage")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.exportedPage)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.exportedRules = QtWidgets.QTextEdit(parent=self.exportedPage)
        self.exportedRules.setObjectName("exportedRules")
        self.verticalLayout_14.addWidget(self.exportedRules)
        self.rightMenuStack.addWidget(self.exportedPage)
        self.importedPage = QtWidgets.QWidget()
        self.importedPage.setObjectName("importedPage")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.importedPage)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.importedRules = QtWidgets.QTextEdit(parent=self.importedPage)
        self.importedRules.setObjectName("importedRules")
        self.verticalLayout_15.addWidget(self.importedRules)
        self.rightMenuStack.addWidget(self.importedPage)
        self.verticalLayout_13.addWidget(self.rightMenuStack)
        self.verticalLayout_12.addWidget(self.rightMenuSubContainer)
        self.horizontalLayout_7.addWidget(self.rightMenuContainer, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_11.addWidget(self.mainBodyContent)
        #self.consoleContainer = QtWidgets.QWidget(parent=self.mainBodyContainer)
        self.consoleContainer = ResizableWidget(self.mainBodyContainer, resizable_edges=[
            QtCore.Qt.Edge.TopEdge
        ])
        self.consoleContainer.setObjectName("consoleContainer")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.consoleContainer)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setSpacing(6)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.consoleSubContainer = QtWidgets.QWidget(parent=self.consoleContainer)
        self.consoleSubContainer.setMinimumSize(QtCore.QSize(0, 150))
        self.consoleSubContainer.setObjectName("consoleSubContainer")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.consoleSubContainer)
        self.verticalLayout_21.setContentsMargins(3, -1, -1, 0)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.consoleFrame = QtWidgets.QFrame(parent=self.consoleSubContainer)
        self.consoleFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.consoleFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.consoleFrame.setObjectName("consoleFrame")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.consoleFrame)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.consoleWidget = QtWidgets.QWidget(parent=self.consoleFrame)
        self.consoleWidget.setObjectName("consoleWidget")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.consoleWidget)
        self.verticalLayout_17.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_17.setSpacing(5)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        # Custom Console Widget        
        self.console = ConsoleWidget(parent=self.consoleWidget)
        self.console.setObjectName("console")
        self.verticalLayout_17.addWidget(self.console)
        self.horizontalLayout_9.addWidget(self.consoleWidget)
        self.verticalLayout_21.addWidget(self.consoleFrame)
        self.verticalLayout_20.addWidget(self.consoleSubContainer)
        self.verticalLayout_11.addWidget(self.consoleContainer)
        self.horizontalLayout.addWidget(self.mainBodyContainer)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1054, 22))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAdd_Rules = QtWidgets.QMenu(self.menuFile)
        self.menuAdd_Rules.setObjectName(u"menuAdd_Rules")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionView_Imported_Rules = QtGui.QAction(parent=MainWindow)
        self.actionView_Imported_Rules.setObjectName("actionView_Imported_Rules")
        self.actionView_Exported_Rules = QtGui.QAction(parent=MainWindow)
        self.actionView_Exported_Rules.setObjectName("actionView_Exported_Rules")
        self.actionImport_Policy = QtGui.QAction(parent=MainWindow)
        self.actionImport_Policy.setObjectName("actionImport_Policy")
        self.actionExport_Policy = QtGui.QAction(parent=MainWindow)
        self.actionExport_Policy.setObjectName("actionExport_Policy")
        self.actionSave_Project = QtGui.QAction(parent=MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionLoad_Project = QtGui.QAction(parent=MainWindow)
        self.actionLoad_Project.setObjectName("actionLoad_Project")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionLoad_syntax = QtGui.QAction(parent=MainWindow)
        self.actionLoad_syntax.setObjectName("actionLoad_syntax")
        self.actionSet_parser = QtGui.QAction(parent=MainWindow)
        self.actionSet_parser.setObjectName("Set_Parser")
        self.actionSet_fieldList = QtGui.QAction(parent=MainWindow)
        self.actionSet_fieldList.setObjectName("Set_fieldList")
        self.actionAdd_Rules_Wizard = QtGui.QAction(MainWindow)
        self.actionAdd_Rules_Wizard.setObjectName(u"actionAdd_Rules_Wizard")
        self.actionAdd_Rules_from_File = QtGui.QAction(MainWindow)
        self.actionAdd_Rules_from_File.setObjectName(u"actionAdd_Rules_from_File")
        self.actionMore_Help = QtGui.QAction(parent=MainWindow)
        self.actionMore_Help.setObjectName("actionMore_Help")
        self.menuFile.addAction(self.actionImport_Policy)
        self.menuFile.addAction(self.actionExport_Policy)
        self.menuFile.addAction(self.menuAdd_Rules.menuAction())
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionLoad_Project)
        self.menuFile.addAction(self.actionExit)
        self.menuAdd_Rules.addAction(self.actionAdd_Rules_Wizard)
        self.menuAdd_Rules.addAction(self.actionAdd_Rules_from_File)
        self.menuView.addAction(self.actionView_Imported_Rules)
        self.menuView.addAction(self.actionView_Exported_Rules)
        self.menuSettings.addAction(self.actionLoad_syntax)
        self.menuSettings.addAction(self.actionSet_parser)
        self.menuSettings.addAction(self.actionSet_fieldList)
        self.menuHelp.addAction(self.actionMore_Help)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.centerMenuStack.setCurrentIndex(1)
        self.rightMenuStack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FWOptimizer"))
        self.leftMenuBtn.setToolTip(_translate("MainWindow", "Menu"))
        
        self.homeBtn.setToolTip(_translate("MainWindow", "Home"))
        self.homeBtn.setText(_translate("MainWindow", "Home"))
        self.homeBtn.originalText = self.homeBtn.text()
        
        self.rulesBtn.setToolTip(_translate("MainWindow", "View Rules"))
        self.rulesBtn.setText(_translate("MainWindow", "Policies"))
        self.rulesBtn.originalText = self.rulesBtn.text()
        
        self.consoleBtn.setToolTip(_translate("MainWindow", "View Reports"))
        self.consoleBtn.setText(_translate("MainWindow", "Console"))
        self.consoleBtn.originalText = self.consoleBtn.text()
        
        self.reportsBtn.setToolTip(_translate("MainWindow", "Information"))
        self.reportsBtn.setText(_translate("MainWindow", "Reports"))
        self.reportsBtn.originalText = self.reportsBtn.text()
        
        self.settingsBtn.setToolTip(_translate("MainWindow", "Settings"))
        self.settingsBtn.setText(_translate("MainWindow", "Settings"))
        self.settingsBtn.originalText = self.settingsBtn.text()
        
        self.helpBtn.setToolTip(_translate("MainWindow", "Help"))
        self.helpBtn.setText(_translate("MainWindow", "Help"))
        self.helpBtn.originalText = self.helpBtn.text()
        
        self.label.setText(_translate("MainWindow", "More Menu"))
        self.closeCenterMenuBtn.setToolTip(_translate("MainWindow", "Close Menu"))
        self.label_2.setText(_translate("MainWindow", "Settings"))
        self.label_4.setText(_translate("MainWindow", "Help"))
        self.title.setText(_translate("MainWindow", "FWOptimizer"))
        self.importBtn.setToolTip(_translate("MainWindow", "Import"))
        self.generateBtn.setToolTip(_translate("MainWindow", "Generate"))
        self.optimizeBtn.setToolTip(_translate("MainWindow", "Optimize"))
        self.viewBtn.setToolTip(_translate("MainWindow", "Visualize"))
        self.exportBtn.setToolTip(_translate("MainWindow", "Export"))
        self.label_5.setText(_translate("MainWindow", "Rules"))
        self.closeRightMenuBtn.setToolTip(_translate("MainWindow", "Close Menu"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAdd_Rules.setTitle(_translate("MainWindow", "Add Rules"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionView_Imported_Rules.setText(_translate("MainWindow", "View Imported Rules"))
        self.actionView_Exported_Rules.setText(_translate("MainWindow", "View Exported Rules"))
        self.actionImport_Policy.setText(_translate("MainWindow", "Import Policy"))
        self.actionExport_Policy.setText(_translate("MainWindow", "Export Policy"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionLoad_Project.setText(_translate("MainWindow", "Load Project"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionLoad_syntax.setText(_translate("MainWindow", "Load syntax"))
        self.actionSet_parser.setText(_translate("MainWindow", "Set Parser"))
        self.actionSet_fieldList.setText(_translate("MainWindow", "Set Field List"))
        self.actionAdd_Rules_Wizard.setText(_translate("MainWindow", "Add Rules Wizard"))
        self.actionAdd_Rules_from_File.setText(_translate("MainWindow", "Add Rules from File"))
        self.actionMore_Help.setText(_translate("MainWindow", "More Help"))