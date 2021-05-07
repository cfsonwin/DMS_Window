# coding=utf-8
import os
import sys

from PyQt5.Qt import *

from Color import ColorList
from DmsForWin import DMS_Function
# from Window import SigSlot
from RegionInfo_Func import Region
from win0408 import Ui_Dialog
import matplotlib

from win0409 import MainDialogImgBW

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】


class MainWin(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        mainWindowColor = "background-color:#FFF0F5"
        self.setStyleSheet(mainWindowColor)
        self.setWindowTitle('Test')
        self.setMinimumSize(900, 600)
        layout_all = QHBoxLayout()
        self.wgt_l = QWidget(self)
        self.wgt_l.setStyleSheet("background-color:#F0F8FF")
        # self.InputWin = SigSlot()
        # wgt_l.setBackgroundRole()
        self.wgt_l.setMinimumWidth(300)
        self.wgt_l.setMaximumWidth(400)
        layout_all.addWidget(self.wgt_l)
        self.wgt_r = QWidget(self)
        self.wgt_r.setMinimumWidth(600)
        self.wgt_l.setMaximumWidth(800)
        self.wgt_r.setStyleSheet("background-color:#F0FFFF")
        layout_all.addWidget(self.wgt_r)
        self.setLayout(layout_all)
        self.LeftWidget()

    def LeftWidget(self):
        lb_leftwidget = QLabel(self.wgt_l)
        lb_leftwidget.setText('生成热点图')
        lw = QWidget(self.wgt_l)
        # lw.setWindowTitle('生成热点图')
        layout_v = QVBoxLayout()
        lw.setLayout(layout_v)

        wgt_1 = QWidget(lw)
        wgt_1_layout = QHBoxLayout()
        wgt_1.setLayout(wgt_1_layout)
        lb1 = QLabel(wgt_1)
        lb1.setText('车型选择：')
        wgt_1_layout.addWidget(lb1)
        wgt_selbtn = QWidget(wgt_1)
        layout_selbtn = QVBoxLayout()
        wgt_selbtn.select_btn_1 = QRadioButton('vx1')
        layout_selbtn.addWidget(wgt_selbtn.select_btn_1)
        wgt_selbtn.select_btn_2 = QRadioButton('j7')
        layout_selbtn.addWidget(wgt_selbtn.select_btn_2)
        wgt_selbtn.select_btn_3 = QRadioButton('ievs4')
        layout_selbtn.addWidget(wgt_selbtn.select_btn_3)
        wgt_selbtn.select_btn_1.toggled.connect(lambda: self.btnstate(wgt_selbtn.select_btn_1))
        wgt_selbtn.select_btn_2.toggled.connect(lambda: self.btnstate(wgt_selbtn.select_btn_2))
        wgt_selbtn.select_btn_3.toggled.connect(lambda: self.btnstate(wgt_selbtn.select_btn_3))
        wgt_selbtn.setLayout(layout_selbtn)
        wgt_1_layout.addWidget(wgt_selbtn)
        layout_v.addWidget(wgt_1)

        wgt_2 = QWidget(lw)
        wgt_2_layout = QVBoxLayout()
        lb2 = QLabel(wgt_2)
        lb2.setText('txt文件路径：')
        wgt_2_layout.addWidget(lb2)
        le = QLineEdit(wgt_2)
        le.setMinimumWidth(280)
        wgt_2_layout.addWidget(le)
        wgt_2.setLayout(wgt_2_layout)
        layout_v.addWidget(wgt_2)

        wgt_3 = QWidget(self)
        wgt_3_layout = QVBoxLayout()
        lb3 = QLabel(wgt_3)
        lb3.setText('xlsx文件路径：')
        wgt_3_layout.addWidget(lb3)
        le_3 = QLineEdit(wgt_3)
        # le_3.resize(500, 20)
        wgt_3_layout.addWidget(le_3)
        wgt_3.setLayout(wgt_3_layout)
        layout_v.addWidget(wgt_3)

        wgt_4 = QWidget(self)
        wgt_4_layout = QVBoxLayout()
        lb4 = QLabel(wgt_4)
        lb4.setText('生成图片名称：')
        wgt_4_layout.addWidget(lb4)
        le_4 = QLineEdit(wgt_3)
        # le_4.resize(500, 20)
        wgt_4_layout.addWidget(le_4)
        wgt_4.setLayout(wgt_4_layout)
        layout_v.addWidget(wgt_4)

        bt = QPushButton(self)
        bt.setText('生成2D-plot')
        bt.setStyleSheet('border-style: solid')
        layout_v.addWidget(bt)
        if wgt_selbtn.select_btn_1.toggled:
            whichcar = wgt_selbtn.select_btn_1.text()
        elif wgt_selbtn.select_btn_2.toggled:
            whichcar = wgt_selbtn.select_btn_2.text()
        elif wgt_selbtn.select_btn_2.toggled:
            whichcar = wgt_selbtn.select_btn_3.text()
        bt.clicked.connect(lambda: self.bt1_func(whichcar, le.text(), le_3.text(), le_4.text()))
        pass
        # split = QSplitter(Qt.Horizontal, self)
        # split.setStyleSheet("Qsplitter::handle(background-color:rgb(200,200,0)")

    def btnstate(self, btn):
        if btn.text() == "vx1":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")
            else:
                print(btn.text() + " is deselected")

        if btn.text() == "j7":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")
            else:
                print(btn.text() + " is deselected")

        if btn.text() == "ievs4":
            if btn.isChecked() == True:
                print(btn.text() + " is selected")
            else:
                print(btn.text() + " is deselected")
    def bt1_func(self, whichcar, lb2text, lb3text, lb4text):
        # if lb2text == '' or lb3text == '' or  lb4text == '':
        #     QMessageBox.warning(self, "警告", "已知条件输入不全！", QMessageBox.Yes, QMessageBox.Yes)
        # elif not os.path.exists(lb2text):
        #     QMessageBox.warning(self, "警告", "txt路径不存在！", QMessageBox.Yes, QMessageBox.Yes)
        # else:
        test = DMS_Function(whichcar, lb2text, lb3text, lb4text )
        # 获取实验数据
        test_time, eye_pos_x = test.GetTestData(16)
        test_time, eye_pos_y = test.GetTestData(17)
        test_time, eye_pos_z = test.GetTestData(18)
        test_time, sight_vec_x = test.GetTestData(19)
        test_time, sight_vec_y = test.GetTestData(20)
        test_time, sight_vec_z = test.GetTestData(21)
        count = 0
        # 遍历每行试验数据
        # 新建图表
        fig1 = MyFigure(width=3, height=2, dpi=100)
        fig1.fig.suptitle(test.graphname)

        for t in range(0, int(len(test_time) / 5)):
            k = 5 * t
            # for k in range(200, 500):
            eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
            sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
            # 实例化区域
            region = Region(test.testtarget, eye_pos, sight_vec)
            # # 新建图表
            colorlist = ColorList()
            if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
                continue
            if count >= 150:
                count = 0
            count += 1
            print('第' + str(k + 1) + '次，处在第' + str(test_time[k]) + '张图片')
            points_test, point_test_extend, sight_point = region.ViewRegion()
            # c_in, c_out = region.PointIn()
            #  for m in range(0, len(points_test)):
            for m in range(0, len(points_test)):
                region_fig = fig1.fig.add_subplot(2, 3, m + 1)
                region_fig.set_title('Region ' + chr(97 + m))
                region_fig.set_xlabel(chr(97 + m) + 'x')
                region_fig.set_ylabel(chr(97 + m) + 'y')
                newcoor = points_test[m]
                newcoor_extend = point_test_extend[m]
                new_inte = sight_point[m]
                b = len(newcoor) - 1
                for a in range(0, len(newcoor)):
                    l_x = np.array([newcoor[b][0], newcoor[a][0]])
                    l_y = np.array([newcoor[b][1], newcoor[a][1]])
                    b = a
                    region_fig.plot(l_x, l_y, color='b')
                b = len(newcoor) - 1
                for a in range(0, len(newcoor_extend)):
                    l_x = np.array([newcoor_extend[b][0], newcoor_extend[a][0]])
                    l_y = np.array([newcoor_extend[b][1], newcoor_extend[a][1]])
                    b = a
                    region_fig.plot(l_x, l_y, color='#483D8B')
                # if m == 4:
                #     region_fig.plot(F_2d_x[k], F_2d_y[k], 'og')
                #     region_fig.plot(new_inte[0], new_inte[1], 'xr')
                if new_inte[0] < 2 and new_inte[0] > -2 and new_inte[1] < 2 and new_inte[1] > -2:
                    region_fig.plot(new_inte[0], new_inte[1], marker='x', color=colorlist[count])
        #D:\pakage\68_0204\2020-09-20-22-40-16\new1.txt
        fig1.show()
        dialog = QDialog(self.wgt_r)
        dialog1 = MainDialogImgBW()
        dialog1.setupUi(dialog)
        dialog1.gridlayout = QGridLayout(dialog1.groupBox)  # 继承容器groupBox
        dialog1.gridlayout.addWidget(fig1, 0, 1)





    def RightWidget(self):

        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = MainWin()
    qb.show()
    sys.exit(app.exec_())
