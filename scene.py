from PyQt5 import QtCore, QtGui, QtWidgets

COLORS = [
    QtGui.QColor(244, 67, 54),  # Red 500
    QtGui.QColor(255, 202, 40),  # Amber 400
    QtGui.QColor(139, 195, 74)  # Light Green 500
]

class AnnotationScene(QtWidgets.QGraphicsScene):

    itemInserted = QtCore.pyqtSignal(QtWidgets.QGraphicsItem)

    def __init__(self, parent=None):
        super(AnnotationScene, self).__init__(parent)
    
        self.image = None
        # self.setPen(QtGui.QPen(COLORS[0], 2, QtCore.Qt.SolidLine,
        #         QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image
    
    def drawImage(self, image):
        self.setImage(image)
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.addPixmap(pixmap)
    
    def drawRect(self, left, top, width, height):
        x1, y1 = left, top
        x2, y2 = x1 + width, y1 + height
        pen = QtGui.QPen(COLORS[1], 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.addLine(x1, y1, x2, y1, pen)
        self.addLine(x2, y1, x2, y2, pen)
        self.addLine(x2, y2, x1, y2, pen)
        self.addLine(x1, y1, x1, y2, pen)

    def mousePressEvent(self, mouseEvent):       
        super(AnnotationScene, self).mousePressEvent(mouseEvent)
    
    def getTestItem(self):
        path = "/home/cuongdd/Datasets/FishData/dotted-data/VPS_CAM34/Lethrinus/VPS_CAM34_38785.jpg"
        image = QtGui.QPixmap(path)
        return image