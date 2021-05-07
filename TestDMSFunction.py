# coding=utf-8


import os

import numpy as np
import numpy.matlib
import xlrd
import xlwt
from matplotlib import pyplot as plt

# from mpl_toolkits import mplot3d
from Color import ColorList
from Color_6 import SixColor
from RegionInfo_Func import Region


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
        self.testtarget = test_target
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
            print('开始初始化... ...')
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
            print('初始化结束。')
        else:
            print('xls已经完成初始化')

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

    def CompareViewDirection(self, show_graph):
        '''
        视线方向比较功能
        :param show_graph: ==1 show图象，其他——》保存图像
        :return: 统计结果_list[str],统计结果矩阵_np矩阵[7*7]
        '''
        # 获取数据
        test_time, test_result = self.GetTestData(22)
        groundtru_time, groundtru_result = self.GetGroundtruthData(1)
        # 数据标准化
        groundtru_result_1 = []
        test_result_1 = []
        for item in test_result:
            if int(item) == 100 or int(item) == 200:
                test_result_1.append(-1)
            else:
                test_result_1.append(item)
        for item in groundtru_result:
            if 'A' in str(item):
                groundtru_result_1.append(0)
            elif 'B' in str(item):
                groundtru_result_1.append(1)
            elif 'C' in str(item):
                groundtru_result_1.append(2)
            elif 'D' in str(item):
                groundtru_result_1.append(3)
            elif 'E' in str(item):
                groundtru_result_1.append(4)
            elif 'F' in str(item):
                groundtru_result_1.append(5)
            elif item == 0 or item == '':
                groundtru_result_1.append(-1)
            else:
                groundtru_result_1.append(6)
        # 测试结果与真值比较，
        Stat = np.matlib.zeros((8, 8))
        for i in range(0, len(test_time)):
            for j in range(0, len(groundtru_time)):
                if test_time[i] == groundtru_time[j]:
                    y1 = int(test_result_1[i]) + 1
                    y2 = int(groundtru_result_1[j]) + 1

                    if y1 == y2:
                        break
                    else:
                        Stat[y2, y1] += 1
                        break
        log = []
        for i in range(1, 8):
            for j in range(1, 8):
                if Stat[i, j] > 10:
                    # print ("Area %d was incorrectly recognized as area %d for %d times" % (i - 1, j - 1, Stat[i, j]))
                    log.append(" %d -> %d for %d times" % (i - 1, j - 1, Stat[i, j]))

        x1 = np.array(test_time)
        y1 = np.array(test_result_1)
        x2 = np.array(groundtru_time)
        y2 = np.array(groundtru_result_1)
        plt.figure(figsize=(16, 7))
        plt.yticks(range(-2, 10))
        plt.xticks(range(0, 350, 10))
        plt.title(self.graphname + 'CompareViewDirection')
        plt.xlabel("Times")
        plt.plot(x1, y1, "or", label='TestData')
        plt.plot(x2, y2, "_b", linewidth=5, label='Groundtruth')
        plt.legend(loc='upper left')
        if show_graph == 1:
            plt.show()
        else:
            plt.savefig(self.graphname + '.png', bbox_inches='tight')
        plt.close()
        return log, Stat

    def FindSix(self):
        test_time1, test_time = self.GetTestData(0)
        test_time1, event_type = self.GetTestData(1)
        test_time1, event_start_time = self.GetTestData(2)
        test_time1, event_end_time = self.GetTestData(3)
        test_time1, view_region = self.GetTestData(9)

        view_rg = []
        tt_dauer = []
        stt = []
        edt = []
        st = 0
        tt_st = 0
        flag = 'err'
        for i in range(0, len(test_time)):

            if int(event_type[i]) == 6:
                '''
                                if first_six ==0:
                    if not event_start_time[i] != 0.0 and event_end_time[i] == 0.0:
                        y1.append(0)
                        first_six += 1
                        pass
                else:
                    if event_start_time[i] != 0.0 and event_end_time[i] == 0.0:
                        y1.append(1)
                    elif event_start_time[i] != 0.0 and event_end_time[i] != 0.0:
                        y1.append(-1)
                '''
                if event_start_time[i] != 0.0 and event_end_time[i] == 0.0:
                    st = event_start_time[i]
                    tt_st = test_time[i]
                    flag = str(view_region[i])
                elif event_start_time[i] != 0.0 and event_end_time[i] != 0.0:
                    if st == event_start_time[i]:
                        tt_ed = test_time[i]
                        view_rg.append(flag)
                        tt_dauer.append(tt_ed - tt_st)
                        stt.append(event_start_time[i])
                        edt.append(event_end_time[i])

                    # y1.append(-1)

        return stt, edt, tt_dauer, view_rg

    # def PointIn2DPlot(self, show_graph):
    #     # 获取实验数据
    #     test_time, eye_pos_x = self.GetTestData(16)
    #     test_time, eye_pos_y = self.GetTestData(17)
    #     test_time, eye_pos_z = self.GetTestData(18)
    #     test_time, sight_vec_x = self.GetTestData(19)
    #     test_time, sight_vec_y = self.GetTestData(20)
    #     test_time, sight_vec_z = self.GetTestData(21)
    #     # test_time, F_2d_x = self.GetTestData(191)
    #     # test_time, F_2d_y = self.GetTestData(192)
    #     # test_time, F_x = self.GetTestData(193)
    #     # test_time, F_y = self.GetTestData(194)
    #     # test_time, F_z = self.GetTestData(195)
    #     count = 0
    #     # 遍历每行试验数据
    #     looplimit = 500
    #     if len(test_time) >= looplimit:
    #         looptimes = int(len(test_time) / looplimit)
    #         for i in range(0, looptimes):
    #             print '打印第' + str(i) + '张图片'
    #             down = 500 * i
    #             up = 500 * i + 500
    #             for j in range(0, 50):
    #                 k = down + 10 * j
    #                 print '打印第' + str(i) + '张图片的第' + str(k - down) + '个点'
    #                 eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
    #                 sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
    #                 # 实例化区域
    #                 region = Region(self.testtarget, eye_pos, sight_vec)
    #                 # 新建图表
    #                 fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
    #                 fig1.suptitle(self.graphname + '_line ' + str(down) + ' to line ' + str(up))
    #                 colorlist = ColorList()
    #                 if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
    #                     continue
    #                 if count >= 150:
    #                     count = 0
    #                 count += 1
    #                 # print '第' + str(k + 1) + '次，处在第' + str(test_time[k]) + '张图片'
    #                 points_test, point_test_extend, sight_point = region.ViewRegion()
    #                 # c_in, c_out = region.PointIn()
    #                 #  for m in range(0, len(points_test)):
    #                 for m in range(0, len(points_test)):
    #                     region_fig = fig1.add_subplot(2, 3, m + 1)
    #                     region_fig.set_title('Region ' + chr(97 + m))
    #                     region_fig.set_xlabel(chr(97 + m) + 'x')
    #                     region_fig.set_ylabel(chr(97 + m) + 'y')
    #                     newcoor = points_test[m]
    #                     newcoor_extend = point_test_extend[m]
    #                     new_inte = sight_point[m]
    #                     b = len(newcoor) - 1
    #                     for a in range(0, len(newcoor)):
    #                         l_x = np.array([newcoor[b][0], newcoor[a][0]])
    #                         l_y = np.array([newcoor[b][1], newcoor[a][1]])
    #                         b = a
    #                         region_fig.plot(l_x, l_y, color='b')
    #                     b = len(newcoor) - 1
    #                     for a in range(0, len(newcoor_extend)):
    #                         l_x = np.array([newcoor_extend[b][0], newcoor_extend[a][0]])
    #                         l_y = np.array([newcoor_extend[b][1], newcoor_extend[a][1]])
    #                         b = a
    #                         region_fig.plot(l_x, l_y, color='#483D8B')
    #                     # if m == 5:
    #                     #     region_fig.plot(new_inte[0], new_inte[1], 'or')
    #                     if new_inte[0] < 2 and new_inte[0] > -2 and new_inte[1] < 2 and new_inte[1] > -2:
    #                         region_fig.plot(new_inte[0], new_inte[1], marker='x', color=colorlist[count])
    #                         #region_fig.plot(new_inte[0], new_inte[1], 'xb')
    #             #plt.show()
    #             plt.savefig(self.graphname + 'from line ' + str(down) + ' to line ' + str(up) + '.png', bbox_inches='tight')
    #             #plt.close()
    #     else:
    #         for k in range(0, len(test_time)):
    #     #   for k in range(125, 140):
    #             eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
    #             sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
    #             # 实例化区域
    #             region = Region(self.testtarget, eye_pos, sight_vec)
    #             vx1_f, Tf = region.GetVX1RegionData(5)
    #             test = np.array([[F_x[k]],[F_y[k]],[F_z[k]]])
    #             f_2d = Tf.dot(test) - Tf.dot(vx1_f[1].reshape([3, 1]))
    #             # 新建图表
    #             fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
    #             fig1.suptitle(self.graphname)
    #             colorlist = ColorList()
    #             if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
    #                 continue
    #             if count >= 150:
    #                 count = 0
    #             count += 1
    #             print '第' + str(k + 1) + '次，处在第' + str(test_time[k]) + '张图片'
    #             points_test, point_test_extend, sight_point = region.ViewRegion()
    #             # c_in, c_out = region.PointIn()
    #             #  for m in range(0, len(points_test)):
    #             for m in range(0, len(points_test)):
    #                 region_fig = fig1.add_subplot(2, 3, m + 1)
    #                 region_fig.set_title('Region ' + chr(97 + m))
    #                 region_fig.set_xlabel(chr(97 + m) + 'x')
    #                 region_fig.set_ylabel(chr(97 + m) + 'y')
    #                 newcoor = points_test[m]
    #                 newcoor_extend = point_test_extend[m]
    #                 new_inte = sight_point[m]
    #                 b = len(newcoor) - 1
    #                 for a in range(0, len(newcoor)):
    #                     l_x = np.array([newcoor[b][0], newcoor[a][0]])
    #                     l_y = np.array([newcoor[b][1], newcoor[a][1]])
    #                     b = a
    #                     region_fig.plot(l_x, l_y, color='b')
    #                 b = len(newcoor) - 1
    #                 for a in range(0, len(newcoor_extend)):
    #                     l_x = np.array([newcoor_extend[b][0], newcoor_extend[a][0]])
    #                     l_y = np.array([newcoor_extend[b][1], newcoor_extend[a][1]])
    #                     b = a
    #                     region_fig.plot(l_x, l_y, color='#483D8B')
    #                 # if m == 4:
    #                 #     region_fig.plot(F_2d_x[k], F_2d_y[k], 'og')
    #                 #     region_fig.plot(new_inte[0], new_inte[1], 'xr')
    #                 if new_inte[0] < 2 and new_inte[0] > -2 and new_inte[1] < 2 and new_inte[1] > -2:
    #
    #                     region_fig.plot(new_inte[0], new_inte[1], marker='x', color=colorlist[count])
    #         if show_graph == 1:
    #             plt.show()
    #         else:
    #             plt.savefig(self.graphname + '_point_location.png', bbox_inches='tight')
    #         plt.close()
    def PointIn2DPlot(self, show_graph):
        # 获取实验数据
        test_time, eye_pos_x = self.GetTestData(16)
        test_time, eye_pos_y = self.GetTestData(17)
        test_time, eye_pos_z = self.GetTestData(18)
        test_time, sight_vec_x = self.GetTestData(19)
        test_time, sight_vec_y = self.GetTestData(20)
        test_time, sight_vec_z = self.GetTestData(21)
        # test_time, F_2d_x = self.GetTestData(191)
        # test_time, F_2d_y = self.GetTestData(192)
        # test_time, F_x = self.GetTestData(193)
        # test_time, F_y = self.GetTestData(194)
        # test_time, F_z = self.GetTestData(195)
        count = 0
        # 遍历每行试验数据
        #
        # 新建图表
        # fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
        # fig1.suptitle(self.graphname)
        for k in range(0, int(len(test_time))):
            # k = 5 * t
            # for k in range(200, 500):
            eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
            sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
            # 实例化区域
            region = Region(self.testtarget, eye_pos, sight_vec)
            # vx1_f, Tf = region.GetVX1RegionData(5)
            # test = np.array([[F_x[k]],[F_y[k]],[F_z[k]]])
            # f_2d = Tf.dot(test) - Tf.dot(vx1_f[1].reshape([3, 1]))
            # # 新建图表
            # fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
            # fig1.suptitle(self.graphname)
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
                # 新建图表
                fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
                fig1.suptitle(self.graphname)

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
                if new_inte[0] < 4 and new_inte[0] > -4 and new_inte[1] < 4 and new_inte[1] > -4:
                    region_fig.plot(new_inte[0], new_inte[1], marker='x', color=colorlist[count])
        if show_graph == 1:
            plt.show()
        else:
            plt.savefig(self.graphname + '_point_location.png', bbox_inches='tight')
        plt.close()

    def PointIn3DPlot(self, show_graph):
        color = SixColor()
        ax = plt.axes(projection='3d')
        test_time, eye_pos_x = self.GetTestData(16)
        test_time, eye_pos_y = self.GetTestData(17)
        test_time, eye_pos_z = self.GetTestData(18)
        test_time, sight_vec_x = self.GetTestData(19)
        test_time, sight_vec_y = self.GetTestData(20)
        test_time, sight_vec_z = self.GetTestData(21)
        x = np.array(eye_pos_x)
        y = np.array(eye_pos_y)
        z = np.array(eye_pos_z)
        # for t in range(0, int(len(test_time) / 3)):
        for k in range(17, 30):
            # k = t * 3
            eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
            sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
            # 实例化区域
            region = Region(self.testtarget, eye_pos, sight_vec)
            if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
                continue
            points_test2d, point_test_extend, sight_point = region.ViewRegion()
            c_in, c_out = region.PointIn()
            notin = 0
            for m in range(0, len(points_test2d)):
                test_region, T = region.Get3DInfo(m)
                j = len(test_region) - 1
                # 三维线的数据
                for i in range(0, len(test_region)):
                    xline = np.array([test_region[i][0], test_region[j][0]])
                    yline = np.array([test_region[i][1], test_region[j][1]])
                    zline = np.array([test_region[i][2], test_region[j][2]])
                    ax.plot3D(xline, yline, zline, color=color[m])
                    j = i
                    i += 1
                if c_in[m] == 0:
                    notin += 1
                    continue
                inte_p = np.array([sight_point[m][0], sight_point[m][1], 0])
                # *******需要改进********

                TT = T.transpose()
                p0 = inte_p.reshape([3, 1])
                p3d = TT.dot(p0) + test_region[1].reshape([3, 1])
                ax.scatter3D(p3d[0], p3d[1], p3d[2], color[m])
            if notin == 6:
                ax.scatter3D(x[k], y[k], z[k], cmap='Greens')
                ax.plot3D(np.array([eye_pos_x[k], eye_pos_x[k] + sight_vec_x[k]]),
                          np.array([eye_pos_y[k], eye_pos_y[k] + sight_vec_y[k]]),
                          np.array([eye_pos_z[k], eye_pos_z[k] + sight_vec_z[k]]), color='#FF0000')
            elif notin == 4:
                ax.scatter3D(x[k], y[k], z[k], cmap='Greens')
                ax.plot3D(np.array([eye_pos_x[k], eye_pos_x[k] + sight_vec_x[k]]),
                          np.array([eye_pos_y[k], eye_pos_y[k] + sight_vec_y[k]]),
                          np.array([eye_pos_z[k], eye_pos_z[k] + sight_vec_z[k]]), color='#000000')
            else:
                ax.scatter3D(x[k], y[k], z[k], cmap='Greens')
                ax.plot3D(np.array([eye_pos_x[k], eye_pos_x[k] + sight_vec_x[k]]),
                          np.array([eye_pos_y[k], eye_pos_y[k] + sight_vec_y[k]]),
                          np.array([eye_pos_z[k], eye_pos_z[k] + sight_vec_z[k]]), color='#00ff00')

        if show_graph == 1:
            plt.show()
        else:
            plt.savefig(self.graphname + '_3D_plot.png', bbox_inches='tight')
        plt.close()

    def PointInNewFigure(self):
        test_time, eye_pos_x = self.GetTestData(16)
        test_time, eye_pos_y = self.GetTestData(17)
        test_time, eye_pos_z = self.GetTestData(18)
        test_time, sight_vec_x = self.GetTestData(19)
        test_time, sight_vec_y = self.GetTestData(20)
        test_time, sight_vec_z = self.GetTestData(21)
        x = []
        y = []

        eye_pos_init = np.array([eye_pos_x[0], eye_pos_y[0], eye_pos_z[0]])
        sight_vec_init = np.array([sight_vec_x[0], sight_vec_y[0], sight_vec_z[0]])
        # if eye_pos_x[0] == 0 and eye_pos_y[0] == 0 and eye_pos_y[0] == 0:
        #     x.append(test_time[0])
        #     y.append(-1)
        # 实例化区域
        region_init = Region(self.testtarget, eye_pos_init, sight_vec_init)
        c_in_init, c_out_init = region_init.PointIn()
        innum = 6
        for m in range(0, 6):
            if c_out_init[m] != 0:
                innum -= 1
                x.append(test_time[0])
                y.append(m)
                break
        if innum == 6:
            x.append(test_time[0])
            y.append(6)
        point_pose_last = int(y[0])
        zero_line = 0
        for k in range(1, len(test_time)):
            print(k)
            eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
            sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
            if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
                zero_line += 1
                x.append(test_time[k])
                y.append(-1)
                last_no_zero = k - zero_line
                point_pose_last = y[last_no_zero]
                continue
            zero_line = 0
            region = Region(self.testtarget, eye_pos, sight_vec)
            c_in, c_out = region.PointIn()
            c_innum = 0
            for item in c_in:
                if item != 0:
                    c_innum += 1
            if c_innum > 1:
                print('qiyi')
            if point_pose_last == 6:
                notin1 = 6
                for m in range(0, 6):
                    if c_in[m] != 0:
                        notin1 -= 1
                        x.append(test_time[k])
                        y.append(m)
                        point_pose_last = m
                    elif c_in[m] == 0 and c_out[m] != 0:
                        notin1 -= 1
                        x.append(test_time[k])
                        y.append(m)
                        point_pose_last = m
                if notin1 == 6:
                    x.append(test_time[k])
                    y.append(6)
                    point_pose_last = 6
            else:
                if c_out[point_pose_last] != 0:
                    x.append(test_time[k])
                    y.append(point_pose_last)
                else:
                    notin = 6
                    for m in range(0, 6):
                        if c_in[m] != 0:
                            notin -= 1
                            x.append(test_time[k])
                            y.append(m)
                            point_pose_last = m
                        elif c_in[m] == 0 and c_out[m] != 0:
                            notin -= 1
                            x.append(test_time[k])
                            y.append(m)
                            point_pose_last = m
                    if notin == 6:
                        x.append(test_time[k])
                        y.append(6)
                        point_pose_last = 6

        return np.array(x), np.array(y)

    def NewRegionTest(self, show_graph, add_test_result):
        x1, new_data = self.PointInNewFigure()

        testdata, orig_result = self.GetTestData(22)
        test_result_1 = []
        for item in orig_result:
            if int(item) == 100 or int(item) == 200:
                test_result_1.append(-1)
            else:
                test_result_1.append(item)
        x2array = np.array(testdata)
        orig_data_array = np.array(test_result_1)
        groundtru_result_1 = []
        plt.plot(x1, new_data, 'xg')
        if add_test_result == 1:
            plt.plot(x2array, orig_data_array, '.r')
        if show_graph == 1:
            plt.show()
        else:
            plt.savefig(self.graphname + '.png', bbox_inches='tight')
        plt.close()
    # def AverageSightPointChangeDistance(self):
    #     test_time, eye_pos_x = self.GetTestData(16)
    #     test_time, eye_pos_y = self.GetTestData(17)
    #     test_time, eye_pos_z = self.GetTestData(18)
    #     test_time, sight_vec_x = self.GetTestData(19)
    #     test_time, sight_vec_y = self.GetTestData(20)
    #     test_time, sight_vec_z = self.GetTestData(21)
    #     eye_pos_init = np.array([eye_pos_x[0], eye_pos_y[0], eye_pos_z[0]])
    #     sight_vec_init = np.array([sight_vec_x[0], sight_vec_y[0], sight_vec_z[0]])
    #     points_test_init, point_test_extend_init, sight_point_init = ViewRegion(self.testtarget, eye_pos_init, sight_vec_init)
    #     sight_point_last = sight_point_init
    #     dist = []
    #     for k in range(1, len(test_time)-1):
    #         eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
    #         sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
    #         if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
    #             continue
    #         if eye_pos_x[k-1] == 0 and eye_pos_y[k-1] == 0 and eye_pos_y[k-1] == 0:
    #             points_test, point_test_extend, sight_point = ViewRegion(self.testtarget, eye_pos, sight_vec)
    #             sight_point_last = sight_point
    #         else:
    #             points_test, point_test_extend, sight_point = ViewRegion(self.testtarget, eye_pos, sight_vec)
    #             notin = 6
    #             for m in range(0, 6):
    #                 newcoor = points_test[m]
    #                 newcoor_extend = point_test_extend[m]
    #                 new_inte = sight_point[m]
    #                 c_in = PointIn(newcoor, new_inte)
    #                 c_out = PointIn(newcoor_extend, new_inte)
    #                 if c_out != 0:
    #                     notin -= 1
    #                     dist.append(np.sqrt(np.square(new_inte[0]-sight_point_last[m][0])+np.square(new_inte[1]-sight_point_last[m][1])))
    #                     sight_point_last = sight_point
    #             if notin == 6:
    #                 sight_point_last = sight_point
    #     dist_sum = 0
    #     dist_max = max(dist)
    #     for item in dist:
    #         dist_sum += item
    #     dist_aver = dist_sum/len(dist)
    #     return dist_aver, dist_max

    # def PointInFigure(self):
    #     test_time, eye_pos_x = self.GetTestData(16)
    #     test_time, eye_pos_y = self.GetTestData(17)
    #     test_time, eye_pos_z = self.GetTestData(18)
    #     test_time, sight_vec_x = self.GetTestData(19)
    #     test_time, sight_vec_y = self.GetTestData(20)
    #     test_time, sight_vec_z = self.GetTestData(21)
    #     for k in range(0, len(test_time)):
    #         eye_pos = np.array([eye_pos_x[k], eye_pos_y[k], eye_pos_z[k]])
    #         sight_vec = np.array([sight_vec_x[k], sight_vec_y[k], sight_vec_z[k]])
    #         fig1 = plt.figure(num=6, figsize=(22, 12), dpi=80)
    #         fig1.suptitle(self.graphname)
    #         if eye_pos_x[k] == 0 and eye_pos_y[k] == 0 and eye_pos_y[k] == 0:
    #             plt.plot(k, -1, 'xr')
    #             print test_time[k], '无数据'
    #             continue
    #         print '第' + str(k + 1) + '次，处在第' + str(test_time[k]) + '张图片'
    #         points_test, point_test_extend, sight_point = ViewRegion(self.testtarget, eye_pos, sight_vec)
    #         for m in range(0, 6):
    #             region_fig = fig1.add_subplot(2, 3, m + 1)
    #             region_fig.set_title('Region ' + chr(97 + m))
    #             newcoor = points_test[m]
    #             newcoor_extend = point_test_extend[m]
    #             new_inte = sight_point[m]
    #             b = len(newcoor) - 1
    #             for a in range(0, len(newcoor)):
    #                 l_x = np.array([newcoor[b][0], newcoor[a][0]])
    #                 l_y = np.array([newcoor[b][1], newcoor[a][1]])
    #                 b = a
    #                 region_fig.plot(l_x, l_y, color='b')
    #             b = len(newcoor) - 1
    #             for a in range(0, len(newcoor_extend)):
    #                 l_x = np.array([newcoor_extend[b][0], newcoor_extend[a][0]])
    #                 l_y = np.array([newcoor_extend[b][1], newcoor_extend[a][1]])
    #                 b = a
    #                 region_fig.plot(l_x, l_y, color='#483D8B')
    #             c_out = PointIn(newcoor_extend, new_inte)
    #             if new_inte[0] < 1.5 and new_inte[0] > -1.5 and new_inte[1] < 1.5 and new_inte[1] > -1.5:
    #                 c_in = PointIn(newcoor, new_inte)
    #                 c_out = PointIn(newcoor_extend, new_inte)
    #                 if c_out == 0:
    #                     region_fig.plot(new_inte[0], new_inte[1], 'xr')
    #                 elif c_in == 0 and c_out != 0:
    #                     region_fig.plot(new_inte[0], new_inte[1], 'xy')
    #                 else:
    #                     region_fig.plot(new_inte[0], new_inte[1], 'xg')
    #
    #     # plt.show()
    #     plt.savefig(self.graphname + '_point_location.png', bbox_inches='tight')
    #

    #

    #


if __name__ == '__main__':
    def test6():
        fp = r'C:\Users\fashu.cheng.HIRAIN\Documents\W10\2021_3_12-dms'
        txtlist = os.listdir(fp)
        wb = xlwt.Workbook()
        for txt in txtlist:
            if 'txt' in txt:
                print('正在处理 ' + txt + '... ...')
                txtpath = os.path.join(fp, txt)
                test = DMS_Function('vx1', txtpath, 'eee', txt)
                stt, edt, tt_dauer, view_rg = test.FindSix()
                print('处理数据中... ...')
                sh = wb.add_sheet(txt, cell_overwrite_ok=True)
                sh.write(0, 0, 'event_st')
                sh.write(0, 1, 'event_ed')
                sh.write(0, 2, 'event_duration')
                sh.write(0, 3, 'event_duration_by_timestamp')
                sh.write(0, 4, 'diff')
                sh.write(0, 5, 'flag')
                for i in range(0, len(stt)):
                    sh.write(i + 1, 0, stt[i])
                    sh.write(i + 1, 1, edt[i])
                    sh.write(i + 1, 2, edt[i] - stt[i])
                    sh.write(i + 1, 3, tt_dauer[i])
                    sh.write(i + 1, 4, tt_dauer[i] - edt[i] + stt[i])
                    sh.write(i + 1, 5, view_rg[i])
            else:
                continue
        wb.save(r'C:\Users\fashu.cheng.HIRAIN\Documents\W10\find6.xls')


    def test6_sta():
        fp = r'C:\Users\fashu.cheng.HIRAIN\Documents\W10\2021_3_12-dms'
        txtlist = os.listdir(fp)
        wb = xlwt.Workbook()
        flag_0 = []
        flag_1 = []
        flag_2 = []
        flag_3 = []
        flag_4 = []
        flag_5 = []
        flag_else = []
        sh0 = wb.add_sheet('0', cell_overwrite_ok=True)
        sh1 = wb.add_sheet('1', cell_overwrite_ok=True)
        sh2 = wb.add_sheet('2', cell_overwrite_ok=True)
        sh3 = wb.add_sheet('3', cell_overwrite_ok=True)
        sh4 = wb.add_sheet('4', cell_overwrite_ok=True)
        sh5 = wb.add_sheet('5', cell_overwrite_ok=True)
        sh_else = wb.add_sheet('else', cell_overwrite_ok=True)
        count0 = 0
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count_else = 0

        for txt in txtlist:
            if 'txt' in txt:
                print('正在处理 ' + txt + ':')
                txtpath = os.path.join(fp, txt)
                test = DMS_Function('vx1', txtpath, 'eee', txt)
                stt, edt, tt_dauer, view_rg = test.FindSix()
                for i in range(0, len(view_rg)):
                    item = float(view_rg[i])
                    if int(item) == 0:
                        print('flag = 0')
                        sh0.write(count0, 0, stt[i])
                        sh0.write(count0, 1, edt[i])
                        sh0.write(count0, 2, edt[i] - stt[i])
                        sh0.write(count0, 3, tt_dauer[i])
                        sh0.write(count0, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh0.write(count0, 5, view_rg[i])
                        count0 += 1
                    elif int(item) == 1:
                        print('flag = 1')
                        sh1.write(count1, 0, stt[i])
                        sh1.write(count1, 1, edt[i])
                        sh1.write(count1, 2, edt[i] - stt[i])
                        sh1.write(count1, 3, tt_dauer[i])
                        sh1.write(count1, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh1.write(count1, 5, view_rg[i])
                        count1 += 1
                    elif int(item) == 2:
                        print('flag = 2')
                        sh2.write(count2, 0, stt[i])
                        sh2.write(count2, 1, edt[i])
                        sh2.write(count2, 2, edt[i] - stt[i])
                        sh2.write(count2, 3, tt_dauer[i])
                        sh2.write(count2, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh2.write(count2, 5, view_rg[i])
                        count2 += 1
                    elif int(item) == 3:
                        print('flag = 3')
                        sh3.write(count3, 0, stt[i])
                        sh3.write(count3, 1, edt[i])
                        sh3.write(count3, 2, edt[i] - stt[i])
                        sh3.write(count3, 3, tt_dauer[i])
                        sh3.write(count3, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh3.write(count3, 5, view_rg[i])
                        count3 += 1
                    elif int(item) == 4:
                        print('flag = 1')
                        sh4.write(count4, 0, stt[i])
                        sh4.write(count4, 1, edt[i])
                        sh4.write(count4, 2, edt[i] - stt[i])
                        sh4.write(count4, 3, tt_dauer[i])
                        sh4.write(count4, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh4.write(count4, 5, view_rg[i])
                        count4 += 1
                    elif int(item) == 5:
                        print('flag = 5')
                        sh5.write(count5, 0, stt[i])
                        sh5.write(count5, 1, edt[i])
                        sh5.write(count5, 2, edt[i] - stt[i])
                        sh5.write(count5, 3, tt_dauer[i])
                        sh5.write(count5, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh5.write(count5, 5, view_rg[i])
                        count5 += 1
                    else:
                        print('flag = else')
                        sh_else.write(count_else, 0, stt[i])
                        sh_else.write(count_else, 1, edt[i])
                        sh_else.write(count_else, 2, edt[i] - stt[i])
                        sh_else.write(count_else, 3, tt_dauer[i])
                        sh_else.write(count_else, 4, (edt[i] - stt[i] - tt_dauer[i] * 1000) / 1000000)
                        sh_else.write(count_else, 5, view_rg[i])
                        count_else += 1

        wb.save(r'C:\Users\fashu.cheng.HIRAIN\Documents\W10\find6_sta.xls')


    def txt2dplot():
        fp = r'C:\Users\fashu.cheng.HIRAIN\Documents\W15\vx1_0423'
        txtlis = os.listdir(fp)
        for txt in txtlis:
            if os.path.splitext(txt)[1] == ".txt":
                txtpath = os.path.join(fp, txt)
                test = DMS_Function('vx1', txtpath, 'ddd', txt[0:-4])
                os.chdir(fp)
                test.PointIn2DPlot(0)


    # fp = r'C:\Users\fashu.cheng.HIRAIN\Documents\W10\2021_3_12-dms\2021_3_12_11_16_44_dms.txt'
    # test = DMS_Function('vx1', fp, 'www', 'qqq')
    # test.GetTestData(0)
    # test6_sta()
    def txtplottestfolder():

        fp = r'D:\0422vx1\20210421-VX1'
        folderlist = os.listdir(fp)
        for folder in folderlist:
            print(folder)
            fp1 = os.path.join(fp, folder)
            txtlis = os.listdir(fp1)
            for txt in txtlis:
                if os.path.splitext(txt)[1] == ".txt":
                    txtpath = os.path.join(fp1, txt)
                    test = DMS_Function('vx1', txtpath, 'ddd', txt[0:-4]+'_new')
                    os.chdir(r'C:\Users\fashu.cheng.HIRAIN\Documents\W15\vx1_0422')
                    test.PointIn2DPlot(0)


    def RTCompare():
        fp = r'C:\Users\fashu.cheng.HIRAIN\Documents\W11\1\1\2021_2_26_16_27_56_dms.txt'
        test = DMS_Function('vx1', fp, 'www', '111')
        test_time, eye_pos_x = test.GetTestData(16)
        test_time, eye_pos_y = test.GetTestData(17)
        test_time, eye_pos_z = test.GetTestData(18)
        test_time, sight_vec_x = test.GetTestData(19)
        test_time, sight_vec_y = test.GetTestData(20)
        test_time, sight_vec_z = test.GetTestData(21)
        p = np.array([eye_pos_x, eye_pos_y, eye_pos_z])
        vec = np.array(([sight_vec_x, sight_vec_y, sight_vec_z]))
        # print(str(p[1][19]))
        R_MMT1 = np.array([[-0.041276, 0.396733, 0.917006],
                           [-0.999052, -0.003707, -0.043366],
                           [-0.013806, -0.917927, 0.396510]])
        T_MMT1 = np.array([[0.869858],
                           [-0.374745],
                           [0.87457]])
        R_PY1 = np.array([[0, 0.39511987, 0.91862957],
                          [-1, 0., 0.],
                          [0, -0.91862957, 0.39511987]])
        T_PY1 = np.array([[0.86873128],
                          [-0.39],
                          [0.87661246]])

        R_MMT2 = np.array([[-0.066687, 0.357190, 0.931648],
                           [-0.997467, -0.000703, -0.071129],
                           [-0.024752, -0.934032, 0.356332]])
        T_MMT2 = np.array([[0.900092],
                           [-0.357170],
                           [0.881658]])
        R_PY2 = np.array([[0, 0.41799519, 0.90844924],
                          [-1, 0., 0.],
                          [0, -0.90844924, 0.41799519]])
        T_PY2 = np.array([[0.88623278],
                          [-0.39],
                          [0.89631814]])

        R_MMT3 = np.array([[-0.051163, 0.393326, 0.917975],
                           [-0.998384, 0.002626, -0.056770],
                           [-0.024740, -0.919396, 0.392556]])
        T_MMT3 = np.array([[0.837695],
                           [-0.365734],
                           [0.858639]])
        R_PY3 = np.array([[0., 0.39496434, 0.91869645],
                          [-1., 0., 0.],
                          [0., -0.91869645, 0.39496434]])
        T_PY3 = np.array([[0.83895561],
                          [-0.39],
                          [0.86373352]])

        R_MMT4 = np.array([[-0.017114, 0.494448, 0.869039],
                           [-0.999794, -0.017987, -0.009455],
                           [0.010957, -0.869021, 0.494654]])
        T_MMT4 = np.array([[0.846263],
                           [-0.407100],
                           [0.832373]])
        R_PY4 = np.array([[0., 0.34562577, 0.93837243],
                          [-1., 0., 0.],
                          [0., -0.93837243, 0.34562577]])
        T_PY4 = np.array([[0.84851183],
                          [-0.39],
                          [0.84524791]])

        R_MMT5 = np.array([[-0.030730, 0.452853, 0.891055],
                           [-0.999473, -0.004614, -0.032124],
                           [-0.010436, -0.891573, 0.452756]])
        T_MMT5 = np.array([[0.888336],
                           [-0.390647],
                           [0.902485]])
        R_PY5 = np.array([[0., 0.34562577, 0.93837243],
                          [-1., 0., 0.],
                          [0., -0.93837243, 0.34562577]
                          ])
        T_PY5 = np.array([[0.90238191],
                          [-0.39],
                          [0.86508959]
                          ])
        k = 0
        sum_p = np.array([[0.0], [0.0], [0.0]])
        sum_theta = 0
        # R_MMT1 = R_MMT2
        # R_PY1 = R_PY2
        # T_MMT1 = T_MMT2
        # T_PY1 = T_PY2
        for i in range(len(test_time)):
            if eye_pos_x[i] == 0 or eye_pos_y[i] == 0 or eye_pos_z[i] == 0:
                continue
            eyepose = np.array([[eye_pos_x[i]], [eye_pos_y[i]], [eye_pos_z[i]]])
            sightvec = np.array(([[sight_vec_x[i]], [sight_vec_y[i]], [sight_vec_z[i]]]))
            p_mmt = R_MMT1.dot(eyepose) + T_MMT1
            p_py = R_PY1.dot(eyepose) + T_PY1
            p_delta = np.abs(p_mmt - p_py)
            sight_mmt = R_MMT1.dot(sightvec)
            sight_py = R_PY1.dot(sightvec)
            len_mmt = np.sqrt(sight_mmt[0] ** 2 + sight_mmt[1] ** 2 + sight_mmt[2] ** 2)
            len_py = np.sqrt(sight_py[0] ** 2 + sight_py[1] ** 2 + sight_py[2] ** 2)
            cos = (sight_mmt[0] * sight_py[0] + sight_mmt[1] * sight_py[1] + sight_mmt[2] * sight_py[2]) / (
                    len_mmt * len_py)
            theta = np.abs(np.arccos(cos))
            sum_p += p_delta
            sum_theta += theta
            k += 1


        delta_aver = sum_p / k
        theta_aver = sum_theta / k
        print(delta_aver)
        print(theta_aver)

    # txt2dplot()
    fp = r'D:\0422vx1\2021_04_23_15_00_55_distract.txt'
    test = DMS_Function('vx1', fp, 'ddd', 'distract')
    test.PointIn3DPlot(1)