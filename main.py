import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui import Ui_MainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import json
from container import Container
from building import Building
import pandas as pd
import math
import copy

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        #This initializes the main window or form

        super().__init__()
        self.setupUi(self)
        
        self.setFixedSize(1560, 900)
        self.setWindowTitle("Warehouse Simulation System")

        self.view = QGraphicsView(self)
        self.view.setFixedSize(1100, 870)
        
        
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-50, -50 ,1060, 500)
        self.scene.addRect(500, 45, 490, 680)
        self.scene.addRect(-15, 0, 490, 800)
        self.view.setScene(self.scene)

        self.containers = {}
        self.lines = []

        with open("./config2.json", "r") as file:
            self.config = json.load(file)
            file.close()


        for data in self.config["dynamic"]["1F"]:
            self.containers[data["num"]] = Container(data, self.scene, floor=1, fix=False)
            self.scene.addItem(self.containers[data["num"]])

        for data in self.config["fix"]["1F"]:
            self.containers[data["num"]] = Container(data, self.scene, floor=1, fix=True)
            self.scene.addItem(self.containers[data["num"]])

        for data in self.config["dynamic"]["2F"]:
            self.containers[data["num"]] = Container(data, self.scene, floor=2, fix=False)
            self.scene.addItem(self.containers[data["num"]])
        
        

        
        

        # with open("config2.json", "w") as file:
        #     json.dump(self.config, file, indent=4, ensure_ascii=False)

        # for i in range(1, 167):
        #     print(self.containers[i].rect().x(), self.containers[i].rect().y())

        # pos correctness virtual position
        for i in range(1, 25):
            self.containers[i].v_pos[0] += self.containers[i].width
        for i in range(45, 65):
            self.containers[i].v_pos[0] += self.containers[i].width

        for i in range(91, 114):
            self.containers[i].v_pos[0] += self.containers[i].width
        for i in range(133, 150):
            self.containers[i].v_pos[0] += self.containers[i].width

        self.containers[65].coordinary = [7.6, 48]
        self.containers[66].coordinary = [7.6, 49.4]

        self.config["dynamic"]["2F"] = []
        for i in range(91, 168):
            data = self.containers[i].output()
            self.config["dynamic"]["2F"].append(data)

        self.config["dynamic"]["1F"] = []
        for i in range(1, 91):
            data = self.containers[i].output()
            self.config["dynamic"]["1F"].append(data)

        self.containers[66].v_pos[0] += self.containers[66].width + 50
        self.containers[66].v_pos[1] += 10
        self.containers[65].v_pos[0] += self.containers[65].width + 50
        self.containers[65].v_pos[1] += 10
        print("66 v_pos : ",self.containers[66].v_pos)
        
        with open("./config2.json", "w") as file:
            json.dump(self.config, file, ensure_ascii=False, indent=4)

        for data in self.config["fix"]["fixarea"]:
            self.scene.addItem(Building(data, self.scene))

        self.newWindow.clicked.connect(self.createNewWindow)
        self.computeLength.clicked.connect(self.computeLengthFunction)
        self.viewBtn.clicked.connect(self.viewFunction)
        self.clear.clicked.connect(self.clearFunction)
        # self.test.clicked.connect(self.testFunction)


        self.sidewalkPoint_1F_L = [[1, 22.5]]
        self.sidewalkPoint_1F_R = [[7.6, 22.5]]
        self.v_sidewalkPoint_1F_L = [[150, 460]]
        self.v_sidewalkPoint_1F_R = [[310, 460]]
        #
        self.sidewalkPoint_2F_L = [[1, 13.5]]
        self.sidewalkPoint_2F_R = [[7.6, 13.5]]
        self.v_sidewalkPoint_2F_L = [[665, 449]]
        self.v_sidewalkPoint_2F_R = [[825, 449]]

        self.parts = []
        self.parts.append([i for i in range(1, 45)])
        self.parts.append([i for i in range(45, 91)])

        self.parts2 = []
        self.parts2.append([i for i in range(91, 94)])
        self.parts2.append([i for i in range(94, 132)])
        self.parts2.append([i for i in range(133, 167)])

        self.windows = []
        
    def createNewWindow(self):
        print("show window")
        window = Window()
        window.show()
        self.windows.append(window)

    def testFunction(self):
        print(self.distanceBetweenTwoPoints1F(self.containers[3], self.containers[67]))
        pass    

    def computeLengthFunction(self):
        pathType = self.pathtype.toPlainText()
        if(pathType == "MTLI"):
            times1F, times2F, length1F, length2F, cross = self.MTLIPath()
        else:
            times1F, times2F, length1F, length2F, cross = self.ZPath()

        velocity = self.velocity.toPlainText()
        if velocity == '':
            velocity = 1
        else:
            velocity = int(velocity)
        
        time = 0
        time1F = length1F / velocity + 20*times1F
        time2F = length2F / velocity + 20*times2F

        self.catchTargetTime1F.setText("1樓揀貨時間 = %.3fs" % time1F)
        self.catchTargetTime2F.setText("2樓揀貨時間 = %.3fs" % time2F)

        if cross:
            self.totalCatchTargetTime1F.setText("總揀貨時間 = %.3fs" % (time1F + time2F + 30))
        else:
            self.totalCatchTargetTime1F.setText("總揀貨時間 = %.3fs" % (time1F + time2F))


    
    def ZPath(self):
        originalOrder1F, seq1F, length1F = self.ZPath1()
        originalOrder2F, seq2F, length2F = self.ZPath2()

        if length1F != 0 and length2F != 0:
            crossFloor = True
        else:
            crossFloor = False
        totalLength = length1F + length2F
        self.pathLength.setText("Path length = %.3fm" % (totalLength))
        self.pathSeq.setText("行走順序 : %s %s" % (str(seq1F), str(seq2F)))
        return originalOrder1F, originalOrder2F, length1F, length2F, crossFloor

    def ZPath1(self):
        order = self.order.toPlainText()
        if order == '':
            return 0, [], 0
        originalOrder = order = order.split(' ')
        order = [int(i) for i in order]
        order = sorted(list(set(order)))

        parts1 = [i for i in order if i in range(1, 25)]
        parts2 = [i for i in order if i in range(25, 45)]
        parts3 = [i for i in order if i in range(45, 67)]
        parts4 = [i for i in order if i in range(67, 91)]

        seq = []
        i = 0
        while i < len(parts1) and i < len(parts2):
            seq.append(parts1[i])
            seq.append(parts2[i])
            i += 1
        
        seq += parts1[i:]
        seq += parts2[i:]

        i = 0
        while i < len(parts3) and i < len(parts4):
            seq.append(parts3[i])
            seq.append(parts4[i])
            i += 1
        
        seq += parts3[i:]
        seq += parts4[i:]


        seq.append(1)
        seq.insert(0, 1)
        points, length = self.lengthOfSequence(seq, 1)
        self.drawPath(points)
        return len(originalOrder), seq, length
        # self.pathLength.setText("Path length = %.3fm" % (length))
        # self.pathSeq.setText("行走順序 :%s" % ())
        pass

    def ZPath2(self):
        order = self.order_2.toPlainText()
        if order == '':
            return 0, [], 0
        originalOrder = order = order.split(' ')
        order = [int(i) for i in order]

        order = sorted(list(set(order)))

        parts1 = [i for i in order if i in range(94, 114)]
        parts2 = [i for i in order if i in range(114, 133)]
        parts3 = [i for i in order if i in range(133, 150)]
        parts4 = [i for i in order if i in range(150, 168)]
        parts5 = [i for i in order if i in range(91, 94)]

        seq = []
        i = 0
        while i < len(parts1) and i < len(parts2):
            seq.append(parts1[i])
            seq.append(parts2[i])
            i += 1
        
        seq += parts1[i:]
        seq += parts2[i:]

        i = 0
        while i < len(parts3) and i < len(parts4):
            seq.append(parts3[i])
            seq.append(parts4[i])
            i += 1
        
        seq += parts3[i:]
        seq += parts4[i:]

        seq += parts5


        seq.append(94)
        seq.insert(0, 94)
        points, length = self.lengthOfSequence(seq, 2)
        self.drawPath(points)
        return len(originalOrder), seq, length
        pass

    def viewFunction(self):
        text = self.sidewalk.toPlainText()
        
        print(text)
        sidewalk = text.split(' ')
        print(sidewalk)
        sidewalk = [int(i) for i in sidewalk if i != ''] 
        i = 0
        while(i < len(sidewalk)):
            self.containers[sidewalk[i]].hide()
            self.containers[sidewalk[i + 1]].hide()
            if sidewalk[i] < 91:
                self.sidewalkPoint_1F_L.append(self.containers[sidewalk[i]].coordinary)
                self.sidewalkPoint_1F_R.append(self.containers[sidewalk[i + 1]].coordinary)
                self.v_sidewalkPoint_1F_L.append(self.containers[sidewalk[i]].v_pos)
                self.v_sidewalkPoint_1F_R.append(self.containers[sidewalk[i + 1]].v_pos)
            else:
                self.sidewalkPoint_2F_L.append(self.containers[sidewalk[i]].coordinary)
                self.sidewalkPoint_2F_R.append(self.containers[sidewalk[i + 1]].coordinary)
                self.v_sidewalkPoint_2F_L.append(self.containers[sidewalk[i]].v_pos)
                self.v_sidewalkPoint_2F_R.append(self.containers[sidewalk[i + 1]].v_pos)
            i += 2

        print(self.sidewalkPoint_1F_L)
        print(self.sidewalkPoint_1F_R)

        order = self.order.toPlainText()
        order = order.split(' ')
        print(order)
        order = [int(i) for i in order if i != '']
        for i in order:
            self.containers[i].setOrder()

        order = self.order_2.toPlainText()
        order = order.split(' ')
        print(order)
        order = [int(i) for i in order if i != '']
        for i in order:
            self.containers[i].setOrder()

    def clearFunction(self):
        for i in self.containers:
            self.containers[i].toNormal()
        self.sidewalkPoint_1F_L = [[1, 22.5]]
        self.sidewalkPoint_1F_R = [[7.6, 22.5]]
        self.v_sidewalkPoint_1F_L = [[150, 434]]
        self.v_sidewalkPoint_1F_R = [[310, 434]]

        self.sidewalkPoint_2F_L = [[1, 13.5]]
        self.sidewalkPoint_2F_R = [[7.6, 13.5]]
        self.v_sidewalkPoint_2F_L = [[665, 449]]
        self.v_sidewalkPoint_2F_R = [[825, 449]]


        for i in range(len(self.lines)):
            self.scene.removeItem(self.lines[i])
        self.lines.clear()
        
    def distanceBetweenTwoPoints1F(self, p1:Container, p2:Container):
        if (p1.num in self.parts[0] and p2.num in self.parts[0]) or (p1.num in self.parts[1] and p2.num in self.parts[1]):
            return [p1.v_pos, p2.v_pos], self.lengthBetweenTwoPoint(p1.coordinary, p2.coordinary)
        elif(p1.num in self.parts[0] and p2.num in self.parts[1]):
            sidewalkIndex, length = self.chooseSideWalk(p1.coordinary, p2.coordinary, self.sidewalkPoint_1F_L, self.sidewalkPoint_1F_R)
            points = []
            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_1F_L[sidewalkIndex])
            points.append(self.v_sidewalkPoint_1F_R[sidewalkIndex])
            points.append(p2.v_pos)
            return points, length + 6.6
        elif(p1.num in self.parts[1] and p2.num in self.parts[0]):
            sidewalkIndex, length = self.chooseSideWalk(p2.coordinary, p1.coordinary, self.sidewalkPoint_1F_L, self.sidewalkPoint_1F_R)
            points = []

            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_1F_R[sidewalkIndex])
            points.append(self.v_sidewalkPoint_1F_L[sidewalkIndex])
            points.append(p2.v_pos)
            return points, length + 6.6
    
    def distanceBetweenTwoPoints2F(self, p1:Container, p2:Container):
        for i in range(len(self.parts)):
            if(p1.num in self.parts2[i] and p2.num in self.parts2[i]):
                return [p1.v_pos, p2.v_pos], self.lengthBetweenTwoPoint(p1.coordinary, p2.coordinary)
        # print('numbers : ', p1.num, p2.num)
        if p1.num in self.parts2[1] and p2.num in self.parts2[2]:
            sidewalkIndex, length = self.chooseSideWalk(p1.coordinary, p2.coordinary, self.sidewalkPoint_2F_L, self.sidewalkPoint_2F_R)
            points = []
            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_2F_L[sidewalkIndex])
            points.append(self.v_sidewalkPoint_2F_R[sidewalkIndex])
            points.append(p2.v_pos)
            # length += 6.6
        elif p1.num in self.parts2[2] and p2.num in self.parts2[1]:
            sidewalkIndex, length = self.chooseSideWalk(p2.coordinary, p1.coordinary, self.sidewalkPoint_2F_L, self.sidewalkPoint_2F_R)
            points = []
            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_2F_R[sidewalkIndex])
            points.append(self.v_sidewalkPoint_2F_L[sidewalkIndex])
            points.append(p2.v_pos)
        elif p1.num in self.parts2[0] and p2.num in self.parts2[2]:
            sidewalkIndex, length = self.chooseSideWalk(p1.coordinary, p2.coordinary, self.sidewalkPoint_2F_L, self.sidewalkPoint_2F_R)
            points = []
            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_2F_L[sidewalkIndex])
            points.append(self.v_sidewalkPoint_2F_R[sidewalkIndex])
            points.append(p2.v_pos)
        elif p1.num in self.parts2[2] and p2.num in self.parts2[0]:
            sidewalkIndex, length = self.chooseSideWalk(p1.coordinary, p2.coordinary, self.sidewalkPoint_2F_L, self.sidewalkPoint_2F_R)
            points = []
            points.append(p1.v_pos)
            points.append(self.v_sidewalkPoint_2F_R[sidewalkIndex])
            points.append(self.v_sidewalkPoint_2F_L[sidewalkIndex])
            points.append(p2.v_pos)
        
        else:
        # elif p1.num in self.parts2[1] and p2.num in self.parts2[0] or p1.num in self.parts2[0] and p2.num in self.parts[1]:
            return [p1.v_pos, p2.v_pos], self.lengthBetweenTwoPoint(p1.coordinary, p2.coordinary)

        return points, length + 6.6

    def chooseSideWalk(self, leftPoint:list, rightPoint:list, sidewalkPoint_L, sidewalkPoint_R):
        minLength = 10000
        minLengthIndex = None
        for i in range(len(sidewalkPoint_L)):
            length1 = self.lengthBetweenTwoPoint(leftPoint, sidewalkPoint_L[i])
            length2 = self.lengthBetweenTwoPoint(rightPoint, sidewalkPoint_R[i])
            totalLength = length1 + length2
            if(totalLength < minLength):
                minLength = totalLength
                minLengthIndex = i
        
        return minLengthIndex, minLength

    def lengthBetweenTwoPoint(self, p1, p2):
        x2 = (p1[0] - p2[0])**2
        y2 = (p1[1] - p2[1])**2
        return math.sqrt(x2 + y2)

    def lengthOfSequence(self, seq, floor):
        points = []
        length = 0
        i = 0
        while(i < len(seq) - 1):
            print("distance Between %d <---> %d" % (seq[i], seq[i+1]))
            if(floor == 1):
                ps ,tempLength = self.distanceBetweenTwoPoints1F(self.containers[seq[i]], self.containers[seq[i + 1]])
            else:
                ps, tempLength = self.distanceBetweenTwoPoints2F(self.containers[seq[i]], self.containers[seq[i + 1]])
            # print("points : ",ps)
            points += ps
            length += tempLength
            i += 1
        return points, length 
    
    def drawPath(self, points):
        i = 0
        while( i < len(points) - 1):
            line = QGraphicsLineItem(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
            line.setPen(QPen(QColor("red")))
            self.scene.addItem(line)
            self.lines.append(line)
            i+= 1

    def MTLIPath1F(self):
        order = self.order.toPlainText()
        originalOrder = order = order.split(' ')
        print(order)
        
        order = list(set(order))
        order = [int(i) for i in order if i != '']
        

        if len(order) == 0:
            return 0, [], 0

        optimalSeq = [1, 1]
        
        i = 0
        while(i < len(order)):
            j = 1
            minLength = 1000000
            seq = copy.deepcopy(optimalSeq)
            print("insert %d" % order[i])
            while(j < len(seq)):
                tempSeq = copy.deepcopy(seq)
                tempSeq.insert(j, order[i])
                print("seq : ", seq)
                print("tempSeq : ",tempSeq)
                # input()
                tempPoints, tempLength = self.lengthOfSequence(tempSeq, 1)
                if(tempLength < minLength):
                    minLength = tempLength
                    optimalSeq = tempSeq
                    optimalPoints = tempPoints
                j+= 1
            print(optimalSeq)
            i += 1
        self.drawPath(optimalPoints)

        return len(originalOrder), optimalSeq, minLength

    def MTLIPath2F(self):
        order = self.order_2.toPlainText()
        originalOrder = order = order.split(' ')
        print(order)

        order = [int(i) for i in order if i != '']
        if len(order) == 0:
            return 0, [], 0

        optimalSeq = [94, 94]
        i = 0
        while(i < len(order)):
            j = 1
            minLength = 1000000
            seq = copy.deepcopy(optimalSeq)
            print("insert %d" % order[i])
            while(j < len(seq)):
                tempSeq = copy.deepcopy(seq)
                tempSeq.insert(j, order[i])
                print("seq : ", seq)
                print("tempSeq : ",tempSeq)
                # input()
                tempPoints, tempLength = self.lengthOfSequence(tempSeq, 2)
                if(tempLength < minLength):
                    minLength = tempLength
                    optimalSeq = tempSeq
                    optimalPoints = tempPoints
                j+= 1
            print(optimalSeq)
            i += 1
        self.drawPath(optimalPoints)

        return len(originalOrder), optimalSeq, minLength

    def MTLIPath(self):
        originalOrder1F, optimalSeq1F, length1F = self.MTLIPath1F()
        originalOrder2F, optimalSeq2F, length2F = self.MTLIPath2F()
        totalLength = length1F + length2F
        if length1F != 0 and length2F != 0:
            crossFloor = True
        else:
            crossFloor = False
        self.pathLength.setText("Path length = %.3fm" % (totalLength))
        self.pathSeq.setText("行走順序 :%s %s" % (str(optimalSeq1F), str(optimalSeq2F)))
        return originalOrder1F, originalOrder2F, length1F, length2F, crossFloor

        # Identify sidewalk

        
if __name__ == '__main__':
    # appctxt = ApplicationContext()
    app = QApplication(sys.argv)
    GUI = Window()
    # GUI2 = Window()
    # view = MyView(GUI)
    GUI.show()
    # exit_code = appctxt.app.exec_()
    sys.exit(app.exec_())

