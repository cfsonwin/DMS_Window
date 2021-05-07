# coding=utf-8
import sys

from PyQt5.Qt import *


# app = QApplication(sys.argv)
# qb = QWidget()
# qb.show()
# sys.exit(app.exec_())
from TestDMSFunction import DMS_Function


class SigSlot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setWindowTitle('Test')
        # self.resize(800, 800)
        # layout_all = QHBoxLayout()
        # wgt_l = QWidget(self)
        # wgt_l.resize(200, 200)
        # layout_all.addWidget(wgt_l)



        layout_v = QVBoxLayout()
        # self.QW_1()



        wgt = QWidget(self)
        layout = QHBoxLayout()
        lb1 = QLabel(wgt)
        lb1.setText('车型选择：')
        layout.addWidget(lb1)
        wgt.select_btn_1 = QRadioButton('vx1')
        layout.addWidget(wgt.select_btn_1)
        wgt.select_btn_2 = QRadioButton('j7')
        layout.addWidget(wgt.select_btn_2)
        wgt.select_btn_3 = QRadioButton('ievs4')
        layout.addWidget(wgt.select_btn_3)
        wgt.select_btn_1.toggled.connect(lambda: self.btnstate(wgt.select_btn_1))
        wgt.select_btn_2.toggled.connect(lambda: self.btnstate(wgt.select_btn_2))
        wgt.select_btn_3.toggled.connect(lambda: self.btnstate(wgt.select_btn_3))
        wgt.setLayout(layout)
        layout_v.addWidget(wgt)

        wgt_2 = QWidget(self)
        layout_2 = QHBoxLayout()
        lb2 = QLabel(wgt_2)
        lb2.setText('txt文件路径：')
        layout_2.addWidget(lb2)
        le = QLineEdit(wgt_2)
        le.resize(500, 20)
        layout_2.addWidget(le)
        wgt_2.setLayout(layout_2)
        layout_v.addWidget(wgt_2)

        wgt_3 = QWidget(self)
        layout_3 = QHBoxLayout()
        lb3 = QLabel(wgt_3)
        lb3.setText('xlsx文件路径：')
        layout_3.addWidget(lb3)
        le_3 = QLineEdit(wgt_3)
        le_3.resize(500, 20)
        layout_3.addWidget(le_3)
        wgt_3.setLayout(layout_3)
        layout_v.addWidget(wgt_3)

        wgt_4 = QWidget(self)
        layout_4 = QHBoxLayout()
        lb4 = QLabel(wgt_4)
        lb4.setText('生成图片名称：')
        layout_4.addWidget(lb4)
        le_4 = QLineEdit(wgt_3)
        le_4.resize(500, 20)
        layout_4.addWidget(le_4)
        wgt_4.setLayout(layout_4)
        layout_v.addWidget(wgt_4)

        bt = QPushButton(self)
        bt.setText('生成2D-plot')
        layout_v.addWidget(bt)
        if wgt.select_btn_1.toggled:
            whichcar = wgt.select_btn_1.text()
        elif  wgt.select_btn_2.toggled:
            whichcar = wgt.select_btn_2.text()
        elif  wgt.select_btn_2.toggled:
            whichcar = wgt.select_btn_3.text()
        bt.clicked.connect(lambda: self.bt1_func(whichcar, le.text(), le_3.text(), le_4.text()))

        self.setLayout(layout_v)


    def bt1_func(self, whichcar, lb2text, lb3text, lb4text):
        test = DMS_Function(whichcar, lb2text, lb3text, lb4text )
        #D:\pakage\68_0204\2020-09-20-22-40-16\new1.txt
        test.PointIn2DPlot(1)



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



app = QApplication(sys.argv)
qb = SigSlot()

qb.show()
sys.exit(app.exec_())
