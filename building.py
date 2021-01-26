from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Building(QGraphicsRectItem):
    def __init__(self, config, scene):
        # self.posx = config["posx"]
        # self.posy = config["posy"]
        self.pos = config["pos"]
        self.width = config["width"]
        self.height = config["height"]
        super().__init__(self.pos[0], self.pos[1], self.width, self.height)
        self.scene = scene
        self.name = config["name"]
        self.text = QGraphicsTextItem()
        self.text.setPlainText(str(self.name))
        self.text.setPos(self.pos[0], self.pos[1] - 4)
        self.scene.addItem(self.text)