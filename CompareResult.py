# coding=utf-8
from datetime import datetime

import numpy as np
import numpy.matlib
import os
import xlwt

from TestDMSFunction import DMS_Function


def TestFolder(testfolder, folderpath):
    '''
    标定值与测试值同时输出在一个坐标系中，x轴为时间戳
    :param testfolder: 68/57
    :param folderpath: 文件夹路径
    :return: 生成log.txt和Statistic Result.xls; 保存对比图片
    '''
    fp = folderpath
    os.chdir(fp)
    pathdir = os.listdir(fp)
    subpath = []
    txtpath = []
    xlsxpath = []
    for folder in pathdir:
        subpath.append(fp + '\\' + folder)
    delfolder = 0
    err_folder = []
    for subfolder in subpath:
        os.chdir(subfolder)
        filedir = os.listdir(subfolder)
        filetype = []
        for i in filedir:
            filetype.append(os.path.splitext(i)[1])
        if '.txt' in filetype and '.xlsx' in filetype:
            delfolder += 1
            for filename in filedir:
                newpath = os.path.join(subfolder, filename)
                if os.path.isfile(newpath):
                    a = 0
                    b = 0
                    if os.path.splitext(newpath)[1] == ".txt":
                        txtpath.append(newpath)
                    if os.path.splitext(newpath)[1] == ".xlsx":
                        xlsxpath.append(newpath)
        else:
            err_folder.append(pathdir[delfolder])
            del (pathdir[delfolder])
    print (err_folder)
    # print txtpath
    # print xlsxpath
    # print filetype
    if testfolder == 57:
        new_result_folder_path = r'C:\Users\fashu.cheng.HIRAIN\Documents\W4\57_result_' + datetime.now().strftime(
            "%m%d_%H%M")
    if testfolder == 68:
        new_result_folder_path = r'C:\Users\fashu.cheng.HIRAIN\Documents\W4\68_result_' + datetime.now().strftime(
            "%m%d_%H%M")
    if not os.path.exists(new_result_folder_path):
        os.makedirs(new_result_folder_path)
    os.chdir(new_result_folder_path)
    wb_result = xlwt.Workbook()
    sh_result = wb_result.add_sheet('sheet1', cell_overwrite_ok=True)
    col = 1
    row = 0
    Stat_all = np.matlib.zeros((8, 8))
    for i in range(0, len(txtpath)):
        test = DMS_Function(0, txtpath[i], xlsxpath[i], pathdir[i])
        result_log, result_stat = test.CompareViewDirection(0)
        #test.PointIn(0)
        Stat_all += result_stat
        sh_result.write(row, 0, pathdir[i])
        for items in result_log:
            sh_result.write(row, col, items)
            col += 1
        row += 1
        col = 1
    txt_file = open(new_result_folder_path + '\\result.txt', 'w')
    txt_file.write('Error Folders are:\n')
    for item in err_folder:
        txt_file.write(item + '\n')
    txt_file.write('Statistic results are:\n')
    for i in range(0, 8):
        for j in range(0, 8):
            if not Stat_all[i, j] == 0:
                print ("Area %d was incorrectly recognized as area %d for %d times" % (i - 1, j - 1, Stat_all[i, j]))
                txt_file.write(
                    "Area %d was incorrectly recognized as area %d for %d times\n" % (i - 1, j - 1, Stat_all[i, j]))
    wb_result.save('Statistic Result.xls')


#TestFolder(68, r'D:\pakage\68_0122')