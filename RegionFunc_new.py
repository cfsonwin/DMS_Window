# coding=utf-8


import numpy as np
import configparser
from PolygonExtend import PolygonExtend


class Region:
    def __init__(self, whichCar, eye_pos, sight_vec):
        self.carname = whichCar
        self.eye_pose = eye_pos
        self.sight_vec = sight_vec
        Coor_info = configparser.ConfigParser()
        Coor_info.read("./config/Coor_info.ini")
        car = Coor_info[self.carname]
        regioninfo = []
        keys_count = int(len(Coor_info.options('vx1')) / 3)
        for i in range(keys_count):
            k1 = 'p' + str(i) + 'x'
            k2 = 'p' + str(i) + 'y'
            k3 = 'p' + str(i) + 'z'
            x = float(car[k1])
            y = float(car[k2])
            z = float(car[k3])
            point = [x, y, z]
            regioninfo.append(point)
            # print(point)
        self.Points = np.array(regioninfo)
        print(regioninfo)

    def PointIn(self):
        '''
        判断视线与平面交点是否在一个特定区域内
        :return: c_in/c_out：值为0时交点不在区域内。
        '''
        all_newcoor, all_newcoor_extend, all_new_inte = self.ViewRegion()
        c_in = []
        c_out = []
        for k in range(0, len(all_newcoor)):
            newcoor = all_newcoor[k]
            new_inte = all_new_inte[k]
            j = len(newcoor) - 1
            zero = 1e-10
            c = 0
            for i in range(0, len(newcoor)):
                cond1 = (newcoor[i][1] >= new_inte[1] and newcoor[j][1] <= new_inte[1]) or (
                        newcoor[i][1] <= new_inte[1] and newcoor[j][1] >= new_inte[1])
                cond2 = np.abs(
                    (new_inte[0] - newcoor[i][0]) * (newcoor[j][1] - newcoor[i][1]) - (
                            new_inte[1] - newcoor[i][1]) * (
                            newcoor[j][0] - newcoor[i][0])) < zero
                cond3 = (newcoor[i][0] >= new_inte[0] and newcoor[j][0] <= new_inte[0]) or (
                        newcoor[i][0] <= new_inte[0] and newcoor[j][0] >= new_inte[0])
                # 判断在不在线上
                if cond1 and cond2 and cond3:
                    c = 0
                    break
                else:
                    cond4 = (newcoor[i][1] >= new_inte[1] and newcoor[j][1] < new_inte[1]) or (
                            newcoor[j][1] >= new_inte[1] and newcoor[i][1] < new_inte[1])
                    if np.abs((newcoor[i][1] - newcoor[j][1])) < zero:
                        cond5 = False
                    else:
                        k = (newcoor[j][0] - newcoor[i][0]) * (new_inte[1] - newcoor[i][1]) / (
                                newcoor[j][1] - newcoor[i][1]) + \
                            newcoor[i][0]
                        cond5 = new_inte[0] < k
                if cond4 and cond5:
                    c = ~c
                j = i
            c_in.append(c)
        for k in range(0, len(all_newcoor)):
            newcoor = all_newcoor_extend[k]
            new_inte = all_new_inte[k]
            j = len(newcoor) - 1
            zero = 1e-10
            c = 0
            for i in range(0, len(newcoor)):
                cond1 = (newcoor[i][1] >= new_inte[1] and newcoor[j][1] <= new_inte[1]) or (
                        newcoor[i][1] <= new_inte[1] and newcoor[j][1] >= new_inte[1])
                cond2 = np.abs(
                    (new_inte[0] - newcoor[i][0]) * (newcoor[j][1] - newcoor[i][1]) - (
                            new_inte[1] - newcoor[i][1]) * (
                            newcoor[j][0] - newcoor[i][0])) < zero
                cond3 = (newcoor[i][0] >= new_inte[0] and newcoor[j][0] <= new_inte[0]) or (
                        newcoor[i][0] <= new_inte[0] and newcoor[j][0] >= new_inte[0])
                # 判断在不在线上
                if cond1 and cond2 and cond3:
                    c = 0
                    break
                else:
                    cond4 = (newcoor[i][1] >= new_inte[1] and newcoor[j][1] < new_inte[1]) or (
                            newcoor[j][1] >= new_inte[1] and newcoor[i][1] < new_inte[1])
                    if np.abs((newcoor[i][1] - newcoor[j][1])) < zero:
                        cond5 = False
                    else:
                        k = (newcoor[j][0] - newcoor[i][0]) * (new_inte[1] - newcoor[i][1]) / (
                                newcoor[j][1] - newcoor[i][1]) + \
                            newcoor[i][0]
                        cond5 = new_inte[0] < k
                if cond4 and cond5:
                    c = ~c
                j = i
            c_out.append(c)
        return c_in, c_out

    def Get3DInfo(self, whichone):
        '''
        pass
        '''
        if self.carname == 1:
            return self.GetVX1RegionData_New(whichone)
        elif self.carname == 0:
            return self.GetVX1RegionData(whichone)
        elif self.carname == 'j7':
            return self.GetJ7RegionData(whichone)
        elif self.carname == 'vx1':
            return self.GetVX1RegionData_Wcs(whichone)
        elif self.carname == 'vx1_car':
            return self.GetVX1RegionData(whichone)
        elif self.carname == 'vx1_new':
            return self.GetVX1RegionData_Wcs_New(whichone)
        elif self.carname == 'ievs4':
            return self.GetIEVS4RegionData(whichone)
        elif self.carname == 'ievs4_test':
            return self.GetIEVS4RegionData_test(whichone)

    def ViewRegion(self):
        '''
        输入眼睛的三维坐标和视线的方向向量，得到各个区域的2d坐标，延伸后区域的2d坐标，视线与平面交点2d坐标
        :param old_new: 用华人运通新数据（=1）；老数据（=0）;J7（=j7）；VX1（=vx1）
        :param eye_pos: 眼睛位置
        :param sight_vec: 视线方向向量
        :return: 各个区域的2d坐标[6*vertxt_num*2]，延伸后区域的2d坐标[6*vertxt_num*2]，视线与平面交点2d坐标[6*2]
        '''
        if self.carname == 1:
            regionextend = self.GetVX1ExtendData_New()
            points_test = self.GetVX1RegionData_New('all')
        elif self.carname == 0:
            regionextend = self.GetVX1ExtendData(1)
            points_test = self.GetVX1RegionData('all')
        elif self.carname == 'j7':
            regionextend = self.GetJ7ExtendData(1)
            points_test = self.GetJ7RegionData('all')
        elif self.carname == 'vx1_car':
            regionextend = self.GetVX1ExtendData(1)
            points_test = self.GetVX1RegionData('all')
        elif self.carname == 'vx1':
            regionextend = self.GetVX1ExtendData_Wcs(1)
            points_test = self.GetVX1RegionData_Wcs('all')
        elif self.carname == 'vx1_new':
            regionextend = self.GetVX1ExtendData_Wcs(0)
            points_test = self.GetVX1RegionData_Wcs_New('all')
        elif self.carname == 'ievs4':
            regionextend = self.GetIEVS4ExtendData()
            points_test = self.GetIEVS4RegionData('all')
        elif self.carname == 'ievs4_test':
            regionextend = self.GetIEVS4ExtendData()
            points_test = self.GetIEVS4RegionData_test('all')
        a = len(points_test)
        sight_point = []
        new2Dcoor = []
        new2Dcoor_extend = []
        for m in range(0, a):
            test_region = points_test[m]
            # 平面法向量
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            # if a > 4:
            #     if m == 0 or m == 2:
            #         v_2 = test_region[3] - test_region[1]
            #     elif m == 1:
            #         v_2 = test_region[4] - test_region[1]
            #     else:
            #         v_2 = test_region[2] - test_region[1]

            v_n = np.cross(v_2, v_1)
            # 坐标系变换矩阵v_1/v_n/v_3
            v_3 = np.cross(v_n, v_2)
            # 单位化坐标系向量，得到平面上点的新的二维坐标
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            T = np.array([v_1, v_2, v_3])
            test = test_region.transpose()
            test1 = T.dot(test) - T.dot(test_region[1].reshape([3, 1]))
            test1 = test1.transpose()
            # 新的坐标系下该区域每个顶点的坐标
            newcoor = []
            for i in range(0, len(test_region)):
                newpoint = []
                for j in range(0, 2):
                    newpoint.append(round(test1[i][j], 3))
                if m == 0:
                    print ('A区域顶点坐标',i, newpoint)
                if m == 1:
                    print ('B区域顶点坐标',i, newpoint)
                if m == 2:
                    print ('C区域顶点坐标',i, newpoint)
                if m == 3:
                    print ('D区域顶点坐标',i, newpoint)
                if m == 4:
                    print ('E区域顶点坐标',i, newpoint)
                if m == 5:
                    print ('F区域顶点坐标',i, newpoint)
                newcoor.append(newpoint)
            new2Dcoor.append(newcoor)
            RegionExtend = PolygonExtend(np.array(newcoor), regionextend[m])
            x, y = RegionExtend.PolygonOutput()
            new2Dcoor_extend.append(np.stack((x, y), axis=-1))
            # 求平面的方程
            points = test_region
            A = (points[1][1] - points[0][1]) * (points[2][2] - points[0][2]) - (points[1][2] - points[0][2]) * (
                    points[2][1] - points[0][1])
            B = (points[2][0] - points[0][0]) * (points[1][2] - points[0][2]) - (points[1][0] - points[0][0]) * (
                    points[2][2] - points[0][2])
            C = (points[1][0] - points[0][0]) * (points[2][1] - points[0][1]) - (points[2][0] - points[0][0]) * (
                    points[1][1] - points[0][1])
            D = -(A * points[0][0] + B * points[0][1] + C * points[0][2])
            plane_normal = np.array([A, B, C])
            para_1 = plane_normal.dot(self.sight_vec)
            para_2 = plane_normal.dot(self.eye_pose) + D
            t = -para_2 / para_1
            p_inte = self.eye_pose + t * self.sight_vec
            # print p_inte
            new_vec = p_inte - self.eye_pose
            p_inte1 = p_inte.reshape([3, 1])
            p_inte_new = T.dot(p_inte1) - T.dot(test_region[1].reshape([3, 1]))
            # 新的坐标系下视线落点的坐标
            new_inte = []
            for i in range(0, 2):

                new_inte.append(np.round(p_inte_new[i], 4))
            sight_point.append(new_inte)
            if m == 0:
                print ('A区域3D交点:', p_inte)
                print ('A区域2D交点:', new_inte)
            if m == 1:
                print ('B区域3D交点:', p_inte)
                print ('B区域2D交点:', new_inte)
            if m == 2:
                print ('C区域3D交点:', p_inte)
                print ('C区域2D交点:', new_inte)
            if m == 3:
                print ('D区域3D交点:', p_inte)
                print ('D区域2D交点:', new_inte)
            if m == 4:
                print ('E区域3D交点:', p_inte)
                print ('E区域2D交点:', new_inte)
            if m == 5:
                print ('F区域3D交点:', p_inte)
                print ('F区域2D交点:', new_inte)



            # if (new_vec[0] > 0 and self.sight_vec[0] < 0) or (new_vec[0] < 0 and self.sight_vec[0] > 0):
            #     sight_point.append([-0.1, -0.1])
            # else:
            #     p_inte1 = p_inte.reshape([3, 1])
            #     p_inte_new = T.dot(p_inte1) - T.dot(test_region[1].reshape([3, 1]))
            #     # 新的坐标系下视线落点的坐标
            #     new_inte = []
            #     for i in range(0, 2):
            #         new_inte.append(round(p_inte_new[i], 4))
            #     sight_point.append(new_inte)
                # print new_inte

        new2Dcoor_array = np.array(new2Dcoor)
        new2Dcoor_extend_array = np.array(new2Dcoor_extend)
        sight_point_array = np.array(sight_point)
        return new2Dcoor_array, new2Dcoor_extend_array, sight_point_array

    def GetVX1RegionData_Wcs(self, region_index):
        '''
        返回各个区域顶点的3d坐标
        :param region_name: 0/1/2/3/4/5/'all'
        :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
        '''
        points_test_B = np.array([[0.725485, -0.669513, 1.193021],
                                  [0.233551, -0.713593, 0.973081],
                                  [0.074801, 0., 0.902105],
                                  [0.092218, 0.356969, 0.909892],
                                  [0.233551, 0.713593, 0.973081],
                                  [0.725485, 0.669513, 1.193021]])
        points_test_D = np.array([[0.724202, -0.593729, 0.94739],
                                  [0.806213, -0.505264, 0.641015],
                                  [0.806057, -0.271242, 0.641598],
                                  [0.723719, -0.12343, 0.949192]])
        points_test_E = np.array([[0.719967, -0.11436, 0.94861],
                                  [1.012212, -0.113104, 0.655121],
                                  [1.02513, 0.685182, 0.642147],
                                  [0.701696, 0.685182, 0.966958]])
        points_test_C = np.array([[1.616849, 0.696711, 1.290307],
                                  [1.554101, 0.825816, 0.974149],
                                  [0.794877, 0.827102, 0.944982],
                                  [0.335786, 0.817187, 0.953351],
                                  [0.847787, 0.73681, 1.166402]])
        points_test_A = np.array([[1.616849, -0.696711, 1.290307],
                                  [1.554101, -0.825816, 0.974149],
                                  [0.794877, -0.827102, 0.944982],
                                  [0.335786, -0.817187, 0.953351],
                                  [0.847787, -0.73681, 1.166402]])
        points_test_F = np.array([[1.749809, 0.609322, 1.433493],
                                  [1.087345, 0.65529, 1.358687],
                                  [1.087861, -0.655578, 1.354122],
                                  [1.750289, -0.609475, 1.429249]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetVX1ExtendData_Wcs(eslf, whichone):
        if whichone == 0:
            regionAchange = np.array([0.05, 0.05, 0.05, 0.05])
            regionBchange = np.array([0.12, 0.25, 0.05, 0.05])
            regionCchange = np.array([0.05, 0.05, 0.05, 0.05])
            regionDchange = np.array([0.05, 0.05, 0.05, 0.12])
            regionEchange = np.array([0.05, 0.05, 0.05, 0.02])
            regionFchange = np.array([0.05, 0.05, 0.05, 0.05])
            regionchange = np.array(
                [regionAchange, regionBchange, regionCchange, regionDchange, regionEchange, regionFchange])
            return regionchange
        else:
            regionAextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionBextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionCextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionDextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionEextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionFextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionextend = np.array(
                [regionAextend, regionBextend, regionCextend, regionDextend, regionEextend, regionFextend])
            return regionextend

    def GetJ7RegionData(self, region_index):
        '''
        返回各个区域顶点的3d坐标
        :param region_name: 0/1/2/3/4/'all'
        :return: A\B\C\D\E\所有 + 对应的转换矩阵
        '''
        points_test_A = np.array([[0.9722, -0.2298, 0.1416], [0.8397, 0.2862, 0.0266], [-0.0078, 0.4387, 0.0370],
                                  [0.0496, -0.0402, 0.1476]])
        points_test_B = np.array([[-0.0351, -0.2672, 0.0426], [-0.0554, 0.1791, -0.111], [-0.4081, 0.2288, 0.0048],
                                  [-0.6924, 0.2963, 0.0882], [-0.8232, 0.2405, 0.1578],
                                  [-0.8908, -0.1387, 0.2673]])
        points_test_C = np.array([[-1.2802, -0.2060, 0.1421], [-1.2302, 0.4299, -0.085], [-1.8238, 0.3982, 0.6973],
                                  [-2.0107, -0.1199, 1.0731]])
        points_test_D = np.array([[-0.1081, 0.1911, 0.1201], [0.0000, 0.5000, 0.1967], [-0.4343, 0.4679, 0.3342],
                                  [-0.4966, 0.2880, 0.2888]])
        points_test_E = np.array([[-0.4852, 0.2084, 0.2830], [-0.4091, 0.5147, 0.3564], [-0.5961, 0.6147, 0.5863],
                                  [-0.8865, 0.1411, 0.6406]])
        points_test = np.array([points_test_A, points_test_B, points_test_C, points_test_D, points_test_E])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetJ7ExtendData(self, whichone):
        if whichone == 0:
            regionAchange = np.array([0, 0, 0, 0])
            regionBchange = np.array([0, 0, 0, 0])
            regionCchange = np.array([0, 0, 0, 0])
            regionDchange = np.array([0, 0, 0, 0])
            regionEchange = np.array([0, 0, 0, 0])
            regionFchange = np.array([0, 0, 0, 0])
            regionchange = np.array(
                [regionAchange, regionBchange, regionCchange, regionDchange, regionEchange, regionFchange])
            return regionchange
        else:
            regionAextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionBextend = np.array([0.03, 0.03, 0.03, 0.03])
            regionCextend = np.array([0.1, 0.1, 0.1, 0.1])
            regionDextend = np.array([0.03, 0.03, 0.03, 0.03])
            regionEextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionextend = np.array(
                [regionAextend, regionBextend, regionCextend, regionDextend, regionEextend])
            return regionextend

    def GetVX1RegionData(self, region_index):
        '''
        返回各个区域顶点的3d坐标
        :param region_name: 0/1/2/3/4/5/'all'
        :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
        '''
        # Hade_pose_system
        # points_test_A = np.array([[0.3070, -0.2139, 0.6865], [0.4742, 0.1490, 0.4898], [0.4755, -0.0860, -0.2327],
        #                           [0.4659, -0.3144, -0.8508], [0.3471, -0.3635, -0.0779]])
        # points_test_B = np.array([[0.3044, -0.3738, 0.1156], [0.3485, -0.3375, -0.4221], [-0.4136, -0.3795, -0.6110],
        #                           [-0.7679, -0.4055, -0.5935], [-0.9748, -0.4318, -0.4042],
        #                           [-0.9075, -0.4534, 0.0369]])
        # points_test_C = np.array([[-1.0881, -0.2294, 0.6390], [-1.2328, 0.0897, 0.4566], [-1.2371, -0.1453, -0.2659],
        #                           [-1.2301, -0.3744, -0.8838], [-1.0934, -0.4989, -0.1918]])
        # points_test_D = np.array([[0.1787, -0.0697, -0.0858], [0.1236, 0.2026, -0.1107], [-0.1736, 0.2026, -0.1107],
        #                           [-0.1666, -0.0710, -0.0856]])
        # points_test_E = np.array([[-0.2586, -0.2600, -0.1374], [-0.2769, 0.2350, 0.0898], [-0.8752, 0.2475, 0.0955],
        #                           [-0.8729, -0.0783, -0.0540]])
        # points_test_F = np.array([[0.1195, -0.3318, 0.6615], [0.01656, -0.4903, 0.0140], [-1.0453, -0.4944, 0.0150],
        #                           [-0.9993, -0.3356, 0.6625]])
        points_test_A = np.array([[0.3067, -0.1521, 0.8767], [0.5309, 0.3428, 0.6372], [0.5322, 0.1078, -0.0853],
                                  [0.5226, -0.1206, -0.7034], [0.3473, -0.3944, -0.1730]])
        points_test_B = np.array([[0.3280, -0.3662, 0.0187], [0.4665, -0.2992, -0.9063], [-0.2956, -0.3412, -1.0954],
                                  [-0.9335, -0.4070, -0.7578], [-1.4371, -0.4382, -0.8270],
                                  [-1.4406, -0.4837, -0.0952]])
        points_test_C = np.array([[-1.1453, -0.1742, 0.3585], [-1.2901, 0.1449, 0.1761], [-1.2943, -0.0901, -0.5364],
                                  [-1.2862, -0.2573, -0.9741], [-1.1872, -0.3245, -0.4058]])
        points_test_D = np.array([[0.2037, -0.0890, -0.0848], [0.1236, 0.3519, -0.1244], [-0.1236, 0.3519, -0.1204],
                                  [-0.2666, -0.0909, -0.0838]])
        points_test_E = np.array([[-0.2756, -0.1414, -0.0830],
                                  [-0.2769, 0.2350, 0.0898],
                                  [-0.8752, 0.2475, 0.0955],
                                  [-0.8718, -0.0328, -0.0331]])
        points_test_F = np.array([[0.2195, -0.2363, 1.0500], [0.2656, -0.3948, 0.4024], [-1.0453, -0.3933, 0.4035],
                                  [-0.9993, -0.2405, 1.0510]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetVX1ExtendData(self, whichone):
        if whichone == 0:
            regionAchange = np.array([0, 0, 0, 0])
            regionBchange = np.array([0, 0, 0, 0])
            regionCchange = np.array([0, 0, 0, 0])
            regionDchange = np.array([0, 0, 0, 0])
            regionEchange = np.array([0, 0, 0, 0])
            regionFchange = np.array([0, 0, 0, 0])
            regionchange = np.array(
                [regionAchange, regionBchange, regionCchange, regionDchange, regionEchange, regionFchange])
            return regionchange
        else:
            regionAextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionBextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionCextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionDextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionEextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionFextend = np.array([0.05, 0.05, 0.05, 0.05])
            regionextend = np.array(
                [regionAextend, regionBextend, regionCextend, regionDextend, regionEextend, regionFextend])
            return regionextend

    def GetVX1RegionData_New(self, region_index):
        '''
        返回各个区域顶点的3d坐标
        :param region_name: 0/1/2/3/4/5/'all'
        :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
        '''
        points_test_A = np.array(
            [[0.30699295, -0.21394505, 0.68641814], [0.4742, 0.149, 0.4898], [0.47550041, -0.08607471, -0.23292968],
             [0.46563566, -0.32222749, -0.87232723], [0.3490371, -0.37039715, -0.11398301]])
        points_test_B = np.array([[0.3044, -0.3738, 0.1156], [0.3485, -0.3375, -0.4221], [-0.4136, -0.3795, -0.6110],
                                  [-0.7679, -0.4055, -0.5935], [-0.9748, -0.4318, -0.4042],
                                  [-0.9075, -0.4534, 0.0369]])
        points_test_C = np.array([[-1.0881, -0.2294, 0.6390], [-1.2328, 0.0897, 0.4566], [-1.2371, -0.1453, -0.2659],
                                  [-1.2301, -0.3744, -0.8838], [-1.0934, -0.4989, -0.1918]])
        points_test_D = np.array(
            [[0.19872336, -0.16873572, -0.07674385], [0.1236, 0.2026, -0.1107], [-0.21341296, 0.2026, -0.1107],
             [-0.20386193, -0.17105986, -0.07653132]])
        points_test_E = np.array([[-0.2586, -0.2600, -0.1374], [-0.2769, 0.2350, 0.0898], [-0.8752, 0.2475, 0.0955],
                                  [-0.8729, -0.0783, -0.0540]])
        points_test_F = np.array([[0.1195, -0.3318, 0.6615], [0.01656, -0.4903, 0.0140], [-1.0453, -0.4944, 0.0150],
                                  [-0.9993, -0.3356, 0.6625]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetVX1ExtendData_New(self):
        regionAextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionBextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionCextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionDextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionEextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionFextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionextend = np.array(
            [regionAextend, regionBextend, regionCextend, regionDextend, regionEextend, regionFextend])
        return regionextend

    def GetVX1RegionData_Wcs_New(self, region_index):
        '''
        返回各个区域顶点的3d坐标
        :param region_name: 0/1/2/3/4/5/'all'
        :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
        '''
        # points_test_B = np.array([[0.725485, -0.669513, 1.193021],
        #                           [0.233551, -0.713593, 0.973081],
        #                           [0.074801, 0., 0.902105],
        #                           [0.092218, 0.356969, 0.909892],
        #                           [0.233551, 0.713593, 0.973081],
        #                           [0.725485, 0.669513, 1.193021]])
        points_test_B = np.array([[0.70735239, -0.669593, 1.18491405],
                                  [-0.00380615, -0.713593, 0.86696041],
                                  [-1.62652855e-01, 4.07000000e-04, 7.95941237e-01],
                                  [-0.14530753, 0.357407, 0.8036962],
                                  [-0.00380615, 0.713407, 0.86696041],
                                  [0.70735239, 0.669407, 1.18491405]])
        # points_test_D = np.array([[0.70389154, -0.61888485, 1.02326542],
        #                           [0.806213, -0.505264, 0.641015],
        #                           [0.80700113, -0.09715478, 0.63807112],
        #                           [0.70860862, -0.13103619, 1.00564388]])
        points_test_D = np.array([[0.74263723, -0.62043125, 0.87852],
                                  [0.84499861, -0.50638409, 0.49612048],
                                  [0.8457865, -0.09839547, 0.49317747],
                                  [0.74745818, -0.13255687, 0.86051048]])

        # points_test_E = np.array([[0.67105565, -0.05940396, 0.99772948],
        #                           [1.012212, -0.113104, 0.655121],
        #                           [1.02513, 0.685182, 0.642147],
        #                           [0.66607658, 0.43978906, 1.00272911]])
        points_test_E = np.array([[0.67783413, -0.05922419, 0.99092214],
                                  [1.012212, -0.113104, 0.655121],
                                  [1.02513, 0.685182, 0.642147],
                                  [0.67320939, 0.44005735, 0.99556594]])
        points_test_C = np.array([[1.616849, 0.696711, 1.290307],
                                  [1.554101, 0.825816, 0.974149],
                                  [0.794877, 0.827102, 0.944982],
                                  [0.335786, 0.817187, 0.953351],
                                  [0.847787, 0.73681, 1.166402]])

        points_test_A = np.array([[1.616849, -0.696711, 1.290307],
                                  [1.554101, -0.825816, 0.974149],
                                  [0.794877, -0.827102, 0.944982],
                                  [0.335786, -0.817187, 0.953351],
                                  [0.847787, -0.73681, 1.166402]])
        points_test_F = np.array([[1.749809, 0.609322, 1.433493],
                                  [0.725485, 0.669513, 1.193021],
                                  [0.725485, -0.669513, 1.193021],
                                  [1.750289, -0.609475, 1.429249]])
        # points_test_F = np.array([[1.749809, 0.609322, 1.433493],
        #                           [1.087345, 0.65529, 1.358687],
        #                           [1.087861, -0.655578, 1.354122],
        #                           [1.750289, -0.609475, 1.429249]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[3] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[4] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[3] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetIEVS4RegionData(self, region_index):
        '''
                返回各个区域顶点的3d坐标
                :param region_name: 0/1/2/3/4/5/'all'
                :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
                '''
        points_test_A = np.array([[0.315426, -0.470126, 0.72184],
                                  [0.347801, -0.016556, 0.675016],
                                  [0.326354, -0.014967, -0.144296],
                                  [0.315579, -0.014168, -0.555904],
                                  [0.315426, -0.167746, -0.129379]])
        # points_test_A = np.array([[0.465426, -0.470126, 0.72184],
        #                           [0.497801, -0.016556, 0.675016],
        #                           [0.476354, -0.014967, -0.144296],
        #                           [0.465579, -0.014168, -0.555904],
        #                           [0.465426, -0.167746, -0.129379]])
        # points_test_A = np.array([[0.31540967, -0.47040324, 0.72199989],
        #                           [0.35149564, 0.03330731, 0.67501599],
        #                           [0.32634338, -0.01496621, -0.14470166],
        #                           [0.3155884, -0.01416938, -0.55556015],
        #                           [0.3154303, -0.16757702, -0.1297068]])
        points_test_B = np.array([[0.204569, -0.470126, 0.20041],
                                  [0.321427, -0.016556, -0.556752],
                                  [-0.238383, 0.024903, -0.625961],
                                  [-0.503428, 0.023399, -0.62345],
                                  [-0.991431, -0.016556, -0.556752],
                                  [-0.874573, -0.470126, 0.20041]])
        points_test_C = np.array([[-0.98543, -0.470126, 0.72184],
                                  [-1.017805, -0.016556, 0.675016],
                                  [-0.996358, -0.014967, -0.144296],
                                  [-0.985582, -0.014168, -0.555904],
                                  [-0.98543, -0.167746, -0.129379]])
        # points_test_C = np.array([[-1.03543, -0.470126, 0.72184],
        #                           [-1.067805, -0.016556, 0.675016],
        #                           [-1.046358, -0.014967, -0.144296],
        #                           [-1.045582, -0.014168, -0.555904],
        #                           [-1.04543, -0.167746, -0.129379]])
        points_test_D = np.array([[0.126268, -0.060496, -0.069751],
                                  [0.126268, 0.05194, -0.057472],
                                  [-0.145223, 0.05194, -0.057472],
                                  [-0.145223, -0.060496, -0.069751]])
        points_test_E = np.array([[-0.248049, -0.055419, -0.131947],
                                  [-0.248049, 0.222748, 0.028727],
                                  [-0.988618, 0.222748, 0.028727],
                                  [-0.988618, -0.055419, -0.131947]])
        points_test_F = np.array([[-0.995596, -0.470681, 0.690109],
                                  [-0.995596, -0.470681, 0.179959],
                                  [0.325592, -0.470681, 0.179959],
                                  [0.325592, -0.470681, 0.690109]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            #v_2 = test_region[4] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetIEVS4RegionData_test(self, region_index):
        '''
                返回各个区域顶点的3d坐标
                :param region_name: 0/1/2/3/4/5/'all'
                :return: A\B\C\D\E\F\所有 + 对应的转换矩阵
                '''
        points_test_A = np.array([[0.31891788, -0.45829532, 0.82120266],
                                  [0.35500874, 0.04548449, 0.77420961],
                                  [0.34085094, -0.00358956, 0.37445932],
                                  [0.32125246, -0.0901948, -0.12634447],
                                  [0.3080236, -0.33995407, -0.07415068]])
        # points_test_A = np.array([[0.31540967, -0.47040324, 0.72199989],
        #                           [0.35149564, 0.03330731, 0.67501599],
        #                           [0.33733387, -0.01578049, 0.27515373],
        #                           [0.31424389, -0.11434385, -0.32463967],
        #                           [0.30100426, -0.36404816, -0.12470849]])
        # points_test_B = np.array([[0.20731432, -0.42346403, 0.12251537],
        #                           [0.28576679, -0.14371476, -0.34448095],
        #                           [-0.80298518, -0.06308281, -0.47908275],
        #                           [-0.85290947, -0.24110507, -0.18190328],
        #                           [-0.45699967, -0.27042578, -0.13295717],
        #                           [-0.48552784, -0.37215279, 0.03685968]])
        points_test_B = np.array([[0.321427, -0.37627887, 0.04374734],
                                  [0.321427, -0.11933396, -0.38518076],
                                  [-0.778573, -0.11933396, -0.38518076],
                                  [-0.778573, -0.2991954, -0.08493109],
                                  [-0.378573, -0.2991954, -0.08493109],
                                  [-0.378573, -0.37627887, 0.04374734]])
        points_test_C = np.array([[-0.98544633, -0.47040324, 0.72199989],
                                  [-1.01411036, 0.03330731, 0.67501599],
                                  [-0.98537813, -0.01578049, 0.27515373],
                                  [-0.94071188, -0.11434385, -0.32463967],
                                  [-0.93783108, -0.36404816, -0.12470849]])
        points_test_D = np.array([[0.226268, -0.04746895, -0.06832833],
                                  [0.226268, 0.35016686, -0.024903],
                                  [-0.173732, 0.35016686, -0.024903],
                                  [-0.173732, -0.04746895, -0.06832833]])
        points_test_E = np.array([[-0.308049, -0.055419, -0.131947],
                                  [-0.308049, 0.222748, 0.028727],
                                  [-0.988618, 0.222748, 0.028727],
                                  [-0.988618, -0.055419, -0.131947]])
        # points_test_F = np.array([[-0.995596, -0.470681, 0.689959],
        #                           [-0.995596, -0.470681, -0.070041],
        #                           [0.325404, -0.470681, -0.070041],
        #                           [0.325404, -0.470681, 0.689959]])
        points_test_F = np.array([[-0.995596, -0.470681, 0.679959],
                                  [-0.995596, -0.470681, -0.320041],
                                  [-0.395596, -0.470681, -0.320041],
                                  [-0.395596, -0.470681, 0.179959],
                                  [0.325404, -0.470681, 0.179959],
                                  [0.325404, -0.470681, 0.679959]])
        points_test = np.array(
            [points_test_A, points_test_B, points_test_C, points_test_D, points_test_E, points_test_F])
        if region_index == 0:
            test_region = points_test[0]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Ta = np.array([v_1, v_2, v_3])
            return points_test_A, Ta
        elif region_index == 1:
            test_region = points_test[1]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tb = np.array([v_1, v_2, v_3])
            return points_test_B, Tb
        elif region_index == 2:
            test_region = points_test[2]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tc = np.array([v_1, v_2, v_3])
            return points_test_C, Tc
        elif region_index == 3:
            test_region = points_test[3]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Td = np.array([v_1, v_2, v_3])
            return points_test_D, Td
        elif region_index == 4:
            test_region = points_test[4]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Te = np.array([v_1, v_2, v_3])
            return points_test_E, Te
        elif region_index == 5:
            test_region = points_test[5]
            v_1 = test_region[0] - test_region[1]
            v_2 = test_region[2] - test_region[1]
            v_n = np.cross(v_2, v_1)
            v_3 = np.cross(v_n, v_2)
            v_1 = v_2 / np.sqrt(np.dot(v_2, v_2))
            v_2 = v_3 / np.sqrt(np.dot(v_3, v_3))
            v_3 = v_n / np.sqrt(np.dot(v_n, v_n))
            Tf = np.array([v_1, v_2, v_3])
            return points_test_F, Tf
        elif region_index == 'all':
            return points_test
        else:
            print ('please enter 0\\1\\2\\3\\4\\5\\all')

    def GetIEVS4ExtendData(self):
        regionAextend = np.array([0.05, 0.05, 0.05, 0.05])
        regionBextend = np.array([0.13, 0.13, 0.05, 0.05])
        regionCextend = np.array([0.1, 0.1, 0.1, 0.1])
        regionDextend = np.array([0.06, 0.06, 0.1, 0.06])
        regionEextend = np.array([0.1, 0.05, 0.05, 0.05])
        regionFextend = np.array([0.08, 0.08, 0.08, 0.08])
        regionextend = np.array(
            [regionAextend, regionBextend, regionCextend, regionDextend, regionEextend, regionFextend])
        return regionextend
