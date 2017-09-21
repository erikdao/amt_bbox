from PyQt5 import QtCore, QtGui, QtWidgets

COLORS = [
    QtGui.QColor(244, 67, 54),  # Red 500
    QtGui.QColor(255, 202, 40),  # Amber 400
    QtGui.QColor(24, 255, 255) # Cyan A200
]

DEFAULT_LINE_WIDTH = 4


class Box(QtWidgets.QGraphicsPathItem):
    selected = QtCore.pyqtSignal(QtWidgets.QGraphicsPathItem)

    def __init__(self, id, geometry, color, brush=None, parent=None):
        super(Box, self).__init__(parent)

        self.id = id
        self.myGeometry = geometry
        self.myColor = color
        self.myBox = None

        self.drawBox(self.myGeometry)
    
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

    def identity(self):
        return self.id
    
    def setColor(self, color):
        self.myColor = color

    def color(self):
        return self.myColor       
    
    def drawBox(self, geometry):
        x, y, width, height = geometry[0], geometry[1], geometry[2], geometry[3]
        path = QtGui.QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x + width, y)
        path.moveTo(x + width, y)
        path.lineTo(x + width, y + height)
        path.moveTo(x + width, y + height)
        path.lineTo(x, y + height)
        path.moveTo(x, y + height)
        path.lineTo(x, y)
        self.setPath(path)        
        # self.myBox = QtWidgets.QGraphicsPathItem(path)
        self.setPen(QtGui.QPen(
            self.myColor, DEFAULT_LINE_WIDTH, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin
        ))
        self.setBrush(QtGui.QBrush(QtCore.Qt.transparent))


class AnnotationScene(QtWidgets.QGraphicsScene):

    itemInserted = QtCore.pyqtSignal(QtWidgets.QGraphicsItem)
    itemSelected = QtCore.pyqtSignal(QtWidgets.QGraphicsItem)

    def __init__(self, parent=None):
        super(AnnotationScene, self).__init__(parent)
    
        self.image = None
        self.box = None

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image
    
    def drawImage(self, image):
        self.setImage(image)
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.addPixmap(pixmap)
    
    def drawRect(self, left, top, width, height, layer=0):
        self.box = Box(geometry=(left, top, width, height), color=COLORS[layer])
        print(self.box.color())
        self.addItem(self.box)

    def mousePressEvent(self, mouseEvent):
        print(self.selectedItems())       
        super(AnnotationScene, self).mousePressEvent(mouseEvent)
    
    def getTestItem(self):
        path = "/home/cuongdd/Datasets/FishData/dotted-data/VPS_CAM34/Lethrinus/VPS_CAM34_38785.jpg"
        image = QtGui.QPixmap(path)
        return image