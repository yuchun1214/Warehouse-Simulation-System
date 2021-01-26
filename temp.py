for i in range(23, 0, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(43, 30, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(63, 50, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(89, 66, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())

self.containers[30].setRect(self.containers[30].rect().x(), self.containers[31].rect().y() + 50, self.containers[30].rect().width(), self.containers[30].rect().height())
for i in range(29, 24, -1):
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 25, self.containers[i].rect().width(), self.containers[i].rect().height())
    print(self.containers[i].rect().y())

self.containers[50].setRect(self.containers[50].rect().x(), self.containers[51].rect().y() + 50, self.containers[50].rect().width(), self.containers[50].rect().height())
for i in range(49, 44, -1):
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 25, self.containers[i].rect().width(), self.containers[i].rect().height())
    print(self.containers[i].rect().y())



for i in range(112, 94, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(131, 118, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(148, 135, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())
for i in range(166, 150, -1):
    print(self.containers[i].rect().y())
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 28, self.containers[i].rect().width(), self.containers[i].rect().height())

self.containers[118].setRect(self.containers[118].rect().x(), self.containers[119].rect().y() + 50, self.containers[118].rect().width(), self.containers[118].rect().height())
for i in range(117, 113, -1):
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 25, self.containers[i].rect().width(), self.containers[i].rect().height())
    print(self.containers[i].rect().y())
self.containers[135].setRect(self.containers[135].rect().x(), self.containers[136].rect().y() + 50, self.containers[136].rect().width(), self.containers[136].rect().height())
for i in range(134, 132, -1):
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 25, self.containers[i].rect().width(), self.containers[i].rect().height())
    print(self.containers[i].rect().y())

self.containers[94].setRect(self.containers[94].rect().x(), self.containers[95].rect().y() + 70, self.containers[94].rect().width(), self.containers[94].rect().height())
for i in range(93, 90, -1):
    self.containers[i].setRect(self.containers[i].rect().x(), self.containers[i + 1].rect().y() + 25, self.containers[i].rect().width(), self.containers[i].rect().height())
    print(self.containers[i].rect().y())

self.containers[150].setRect(self.containers[150].rect().x(), self.containers[133].rect().y(), self.containers[150].rect().width(), self.containers[150].rect().height())



coordy = 0
for i in range(1, 25):
    self.containers[i].coordinary = [0, coordy]
    coordy += 2
coordy = 0
for i in range(67, 91):
    self.containers[i].coordinary = [8.6, coordy]
    coordy += 2

coordy = 46
for i in range(44, 30, -1):
    self.containers[i].coordinary = [1, coordy]
    coordy -= 2
coordy = 46
for i in range(64, 50, -1):
    self.containers[i].coordinary = [7.6, coordy]
    coordy -= 2

coordy = 19
for i in range(30, 24, -1):
    self.containers[i].coordinary = [1, coordy]
    coordy -= 2
coordy = 19
for i in range(50, 44, -1):
    self.containers[i].coordinary = [7.6, coordy]
    coordy -= 2

coordy = 40
for i in range(113, 94, -1):
    self.containers[i].coordinary = [0, coordy]
    coordy -= 2
coordy -= 2
for i in range(94, 90, -1):
    self.containers[i].coordinary = [0, coordy]
    coordy -= 2

coordy = 40
for i in range(167, 149, -1):
    self.containers[i].coordinary = [8.6, coordy]
    coordy -= 2

coordy = 40
for i in range(132, 118, -1):
    self.containers[i].coordinary = [1, coordy]
    coordy -= 2
coordy = 40
for i in range(149, 135, -1):
    self.containers[i].coordinary = [7.6, coordy]
    coordy -= 2

coordy = 13
for i in range(118, 113, -1):
    self.containers[i].coordinary = [1, coordy]
    coordy -= 2
coordy = 13
for i in range(135, 132, -1):
    self.containers[i].coordinary = [7.6, coordy]
    coordy -= 2