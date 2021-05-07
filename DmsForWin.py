# coding=utf-8


import numpy as np
import numpy.matlib
import xlrd
import xlwt
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
# from mpl_toolkits import mplot3d
from Color import ColorList
from RegionInfo_Func import Region
from Color_6 import SixColor
import os
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from win0409 import MyFigure

class DMS_Function:
    '''
    生成比较结果
    '''
    filename = str  # 文件夹名称

    def __init__(self, test_target, testdataadr, groundtruthadr, graphname):
        '''
        :param test_target: 测试项目：‘0’或‘1’或‘J7’或‘vx1’
        :param testdataadr: 算法生成的txt文件夹路径
        :param groundtruthadr: 标定结果Excel表格路径
        :param graphname: 生成的图像的名称
        完成初始化，将txt文件中的数据重新整理成Excel表格形式
        '''
        # print 'Process being initialized... ...'
        self.testtarget =  test_target
        self.testdataadr = testdataadr
        self.groundtruthadr = groundtruthadr
        self.graphname = graphname
        # folderpath = os.path.abspath(testdataadr)
        # xlspath = os.path.join(folderpath, DMS_Function.filename)
        # 获取txt文件每列数据对应的测试项目名称

        DMS_Function.filename = self.testdataadr[0:-4] + '_test_data' + '.xls'
        # os.path.dirname(self.testdataadr)
        # excelpath = os.path.join(testdataadr)
        if not os.path.exists(DMS_Function.filename):
            print ('开始初始化... ...')
            wb_type = xlrd.open_workbook('C:/Users/fashu.cheng.HIRAIN/Documents/python_Compare/type.xlsx')
            sheet_type = wb_type.sheet_by_name('type')
            type_keyword = []
            for items in sheet_type.col_values(1):
                items = items.strip().encode('raw_unicode_escape')
                type_keyword.append(items)
            del (type_keyword[0])
            x = 0
            y = 0
            xls = xlwt.Workbook()
            sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
            for i in range(0, len(type_keyword)):
                sheet.write(x, i, str(type_keyword[i]))
            # 将当前测试组的txt文件数据列入对应位置
            x = 1
            file = open(self.testdataadr, 'r')
            while True:
                lines = file.readline()
                if not lines:
                    break
                for i in lines.split(','):
                    item = i.strip().encode('utf8').decode('utf8')
                    sheet.write(x, y, item)
                    y += 1
                x += 1
                y = 0
            file.close()
            xls.save(DMS_Function.filename)
            print( '初始化结束。')
        else:
            print ('xls已经完成初始化')

    def GetTestData(self, testnum):
        '''
        得到测试数据
        :param testnum: 测试项目序号 22=视线方向; 1=输出了6 2=输出的开始时间 3=输出的结束时间
        :return: 时间序列_list[int]，测试结果_list[float]
        '''
        # print 'Getting test data... ...'
        workbook = xlrd.open_workbook(DMS_Function.filename)
        sheet_new = workbook.sheet_by_name('sheet1')
        new_time = []
        for item in sheet_new.col_values(0):
            item = item.strip().encode('raw_unicode_escape')
            new_time.append(item)
        del (new_time[0])
        time2 = []
        i = 1
        # print new_time
        for item in new_time:

            # item = item.strip(b'\x00'.decode())
            # print item
            # if item == '':
            #     break
            item = float(item)
            item = round((item - float(new_time[0])) / (1000 / 30))
            item = int(item)
            i += 1
            time2.append(item)

        test_item = []
        for item in sheet_new.col_values(testnum):
            item = item.strip().encode('raw_unicode_escape')
            test_item.append(item)
        del (test_item[0])

        test_item_new = []
        for item in test_item:
            item = float(item)
            test_item_new.append(item)
        count_new = time2[95:229]
        test_item_new1 = test_item_new[95:229]
        return time2, test_item_new
        # return count_new, test_item_new1

    def GetGroundtruthData(self, testitem):
        '''
        得到真值
        :param testitem: 项目真值序号 1=视线方向
        :return: 数据序列_list[int],真值list[]
        '''
        # print 'Getting groundtruth data... ...'
        workbook_true = xlrd.open_workbook(self.groundtruthadr)
        sheet_true = workbook_true.sheet_by_index(0)
        count = []

        for item in sheet_true.col_values(0):
            # item = item.strip().encode('raw_unicode_escape')
            count.append(item)
        del (count[0:8])

        for i in range(0, 299):
            count[i] = int(count[i])
        test_item = []
        for item in sheet_true.col_values(testitem):
            test_item.append(item)
        del (test_item[0:8])

        return count, test_item

    def PointIn2DPlot(self):
        # 获取实验数据
        test_time, eye_pos_x = self.GetTestData(16)
        test_time, eye_pos_y = self.GetTestData(17)
        test_time, eye_pos_z = self.GetTestData(18)
        test_time, sight_vec_x = self.GetTestData(19)
        test_time, sight_vec_y = self.GetTestData(20)
        test_time, sight_vec_z = self.GetTestData(21)
        count = 0
        # 遍历每行试验数据
        # 新建图表
        fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
        fig1.suptitle(self.graphname)

        for t in range(0, int(len(test_time) / 5)):
            k = 5 * t
            # for k in range(200, 500):
            eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
            sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
            # 实例化区域
            region = Region(self.testtarget, eye_pos, sight_vec)
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
                region_fig = fig1.add_subplot(2, 3, m + 1)
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
        return fig1