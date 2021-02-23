from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Container(QGraphicsRectItem):
    def __init__(self, config, scene, floor=None, fix=False):
        # self.posx = config["posx"]
        # self.posy = config["posy"]
        self._pos = config["pos"]
        self.width = config["width"]
        self.height = config["height"]
        self.size = config["size"]

        try:
            self.coordinary = config["coordinary"]
            # print(self.coordinary)
        except:
            self.coordinary = [0, 0]

        super().__init__(0, 0, self.width, self.height)
        self.setPos(self._pos[0], self._pos[1])
        # self.setPos(self._pos[0], self._pos[1])
        self.scene = scene
        self.num = config["num"]
        self.text = QGraphicsTextItem()
        # self.text.setPlainText(str(self.num) + " (%.1f, %.1f)" % (self.coordinary[0], self.coordinary[1]))
        self.text.setPlainText(str(self.num))
        self.text.setPos(self._pos[0], self._pos[1] - 4)
        self.scene.addItem(self.text)
        self.floor = floor
        self.fix = fix
        self._brush = QBrush()
        self._pen = QPen(QColor("black"))
        self._pen.setWidth(1)
        self.setPen(self._pen)
        self.setBrush(self._brush)
        self.isOrder = False
        self.v_pos = self._pos
        self.distance = 0
        self.isSideWalk = False


    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rect(), self._brush)
        painter.drawRect(self.rect())

    def setOrder(self):
        self.isOrder = True
        self._brush = QColor(250, 235, 215, 232)
        self.update()
        
    def hide(self):
        super().hide()
        self.text.hide()

    def setColor(self, color):
        self._brush = color
        self.update()

    def output(self):
        self._pos = [self.pos().x(), self.pos().y()]
        
        return {
            "num" : self.num,
            "width" : self.width,
            "height" : self.height,
            "size" : self.size,
            "pos" : self._pos,
            "coordinary" : self.coordinary
        }

    def show(self):
        super().show()
        self.text.show()

    def toNormal(self):
        self.show()
        self.isOrder = False
        self.isSideWalk = False
        self._brush = QBrush()
        self.update()

    def setSidewalk(self):
        self.hide()
        self.isSideWalk = True
