# coding=utf-8
import numpy as np
from RegionInfo_Func import Region
from PolygonExtend import PolygonExtend
def RegionChange(region_index, region_change):
    '''
    输入想要改变的区域的代号以及四个方向想要改变的距离
    :param region_index: 0-A; 1-B; 2-C; 3-D; 4-E; 5-F
    :param region_change: np.array([4,1])
    :return: 新的三维坐标
    '''

    eye_pos = np.array([0, 0, 0])
    sight_vec = np.array([1, 1, 1])
    region = Region(0, eye_pos, sight_vec)
    test_region, T = region.GetVX1RegionData(region_index)
    Tt = T.transpose()
    new2Dcoor, new2Dcoor_extend, sight_point = region.ViewRegion()
    test = PolygonExtend(new2Dcoor[region_index], region_change)
    x, y = test.PolygonOutput()
    new_vertex = []
    for i in range(0, len(x)):
        point_new = np.array([x[i], y[i], 0])
        p0 = point_new.reshape([3, 1])
        p3d = Tt.dot(p0) + test_region[1].reshape([3, 1])
        p3d1 = p3d.reshape([1, 3])
        new_vertex.append(p3d1[0])
    vertax_array = np.array(new_vertex)
    return vertax_array



