#-*-: encoding: utf-8
import os
from PyQt5 import QtCore, QtGui, QtWidgets

import resources
from scene import AnnotationScene
from utils import load_amt_csv


class MainWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    dirTreeViewSelectionChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initProps()        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createToolBox()

        self.createGraphicsScene()
        self.createGraphicsView()

        self.createInspectorToolBox()
    
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.toolBox)
        layout.addWidget(self.view)
        layout.addWidget(self.propsInspector)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)

        icon = QtGui.QIcon(':/image/icon.ico')
        self.setWindowIcon(icon)
        self.setWindowTitle("Visual FX (Beta)")

        self.connectEvents()

    def initProps(self):
        self.csvFileName = None
        self.annotation_data = list()
    
    def connectEvents(self):
        self.resized.connect(self.onWindowResized)

    def setActiveImage(self, in_image):
        if isinstance(in_image, QtGui.QImage):
            image = in_image
        else:
            image = QtGui.QImage(in_image)
        self.scene.clear()
        self.scene.drawImage(image)
        self.fitImageToCurrentWindow()

    def fitImageToCurrentWindow(self):
        """Get the image nicely fit in current windows size"""
        if not self.scene.getImage():
            return
        w, h = self.scene.getImage().width(), self.scene.getImage().height()
        self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()

    def openImageHandler(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image',
            '/home/cuongdd/', "Image files (*.jpg *.png)")
        if path:
            if os.path.exists(path[0]):
                self.setActiveImage(path[0])    
    
    def openFolderHandler(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Folder', '/home/cuongdd/')
        if path:
            if os.path.isdir(path):
                self.setUpFileDirModel(path)
    
    def setUpFileDirModel(self, path):
        path = path + "/"
        print(path)
        self._setUpDirModel(path)
        self._setupFileModel(path)
    
    def _setupFileModel(self, path):
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.fileModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.fileModel.setRootPath(path)
    
    def _setUpDirModel(self, path):
        self.dirModel = QtWidgets.QFileSystemModel(self)
        self.dirModel.setReadOnly(True)
        self.dirModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)
        # self.dirModel.setNameFilters(["*.jpg"])
        # self.dirModel.setNameFilterDisables(False)        
        index = self.dirModel.setRootPath(path)
        # self.dirModel.selectionChanged.connect(self.onDirTVSelectionChanged)        
        
        self.dirTreeView.setModel(self.dirModel)
        self.dirTreeView.setRootIndex(index)
        self.dirTreeView.expand(index)
        self.dirTreeView.resizeColumnToContents(0)

        self.dirTreeView.hideColumn(1)  # Hide Size
        self.dirTreeView.hideColumn(2)  # Hide Data Type
        self.dirTreeView.hideColumn(3)  # Hide Date

        self.dirTreeView.selectionModel().selectionChanged.connect(self.onDirTVSelectionChanged)        

    def setCSVFile(self, path):
        file_name = os.path.basename(path)
        self.csvFileName = file_name
        self.csvFileLabel.setText(file_name)
        self.annotation_data = load_amt_csv(path)

    def saveImageHandler(self):
        pass        
    
    def saveAnnotationHandler(self):
        pass
    
    def addBoundingBoxHandler(self):
        print("Draw Bounding Box...")
    
    def addTextHandler(self):
        print("Add Text...")
    
    def importCSVHandler(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open AMT CSV file',
            'home/cuongdd/', "Text files (*.csv *json *.txt)")
        if path:
            if os.path.exists(path[0]) and path[0].endswith('.csv'):
                self.setCSVFile(path[0])
    
    def about(self):
        print("IVUL VisualFX")

    def createActions(self):
        self.openImageAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/open_image.svg'), "Open Image...",
            self, shortcut="Ctrl+O", statusTip="Open an Image",
            triggered=self.openImageHandler)
        
        self.openFolderAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/open_folder.svg'), "Open Folder...",
            self, shortcut="Ctrl+D", statusTip="Open a Folder",
            triggered=self.openFolderHandler
        )

        self.saveImageAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/save_image.svg'), "Save Image...",
            self, shortcut="Ctrl+S", statusTip="Save current image with annotation",
            triggered=self.saveImageHandler
        )

        self.saveAnnotationAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/save_annotation.svg'), "Save Annotation...",
            self, shortcut="Ctrl+Shift+S", statusTip="Save annotation",
            triggered=self.saveAnnotationHandler
        )

        self.importCSVAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/import_csv.svg'), "Import AMT CSV...",
            self, shortcut="Ctrl+I", statusTip="Import Amazon Mechanical Turk CSV File",
            triggered=self.importCSVHandler
        )

        self.drawBoundingBoxAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/draw_bounding_box.svg'), "Draw bounding box",
            self, shortcut="Ctrl+Shift+B", statusTip="Draw bounding box",
            triggered=self.addBoundingBoxHandler
        )

        self.addTextAction = QtWidgets.QAction(
            QtGui.QIcon(':/images/add_text.svg'), "Add text",
            self, shortcut="Ctrl+Shift+T", statusTip="Add text",
            triggered=self.addTextHandler
        )

        self.quitAction = QtWidgets.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit VisualFX", triggered=self.close)

        self.aboutAction = QtWidgets.QAction("&About", self, triggered=self.about)
 

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openImageAction)
        self.fileMenu.addAction(self.openFolderAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importCSVAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveImageAction)
        self.fileMenu.addAction(self.saveAnnotationAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)

    def createGraphicsScene(self):
        # Main Scene
        self.scene = AnnotationScene()
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 5000, 5000))
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.transparent))
    
    def createGraphicsView(self):
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.openImageAction)
        self.fileToolBar.addAction(self.openFolderAction)
        self.fileToolBar.addAction(self.importCSVAction)

        self.fileToolBar = self.addToolBar("Save")
        self.fileToolBar.addAction(self.saveImageAction)
        self.fileToolBar.addAction(self.saveAnnotationAction)

        self.annotationToolBar = self.addToolBar("Annotation")
        self.annotationToolBar.addAction(self.drawBoundingBoxAction)
        self.annotationToolBar.addAction(self.addTextAction)

    def createToolBox(self):
        self.csvGroupBox = QtWidgets.QGroupBox("AMT Results")
        csvLayout = QtWidgets.QHBoxLayout()
        self.csvFileLabel = QtWidgets.QLabel(self.csvFileName)
        csvLayout.addWidget(self.csvFileLabel)
        self.csvGroupBox.setLayout(csvLayout)

        self.dirTreeView = QtWidgets.QTreeView()
        self.dirTreeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.csvGroupBox)        
        layout.addWidget(self.dirTreeView)

        itemWidget = QtWidgets.QWidget()
        itemWidget.setLayout(layout)

        self.toolBox = QtWidgets.QToolBox()
        self.toolBox.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Ignored))
        self.toolBox.setMinimumWidth(350)
        self.toolBox.addItem(itemWidget, "Files")

    def createInspectorToolBox(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("There is nothing to show"))

        itemWidget = QtWidgets.QWidget()
        itemWidget.setLayout(layout)

        self.propsInspector = QtWidgets.QToolBox()
        self.propsInspector.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Ignored))
        self.propsInspector.setMinimumWidth(300)
        self.propsInspector.addItem(itemWidget, "Property Inspector")      

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def onWindowResized(self):
        self.fitImageToCurrentWindow()

    def onDirTVSelectionChanged(self, event):
        index = self.dirTreeView.currentIndex()
        path = self.dirModel.filePath(index)
        self.setActiveImage(path)
        item = self.getAnnotationByImageUrl(path)
        anno = item['annotations'][0]
        self.scene.drawRect(anno['left'], anno['top'], anno['width'], anno['height'])

    # Annotation-related method
    def getAnnotationByImageUrl(self, url):
        return list(filter(lambda item: item['image_url'] == url, self.annotation_data))[0]

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 1280, 720)
    mainWindow.show()

    sys.exit(app.exec_())
