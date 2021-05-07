# coding=utf-8
import numpy as np


class PolygonExtend:
    def __init__(self, vertex, distance):
        '''
        2d平面多边形向外延申一定距离
        :param vertex: 多边形顶点坐标
        :param distance: 左上右下四个方向平移的距离
        '''
        self.vertex = vertex
        self.distance = distance

    def node_inter(self, a, b, c, d):
        '''
        输入两条直线上各两个点，得到交点
        :param a: line1 point1
        :param b: line1 point2
        :param c: line2 point1
        :param d: line2 point1
        :return: 两条直线交点
        '''
        A0 = float(a[1] - b[1])
        B0 = float(b[0] - a[0])
        C0 = float(a[0] * b[1] - b[0] * a[1])
        A1 = float(c[1] - d[1])
        B1 = float(d[0] - c[0])
        C1 = float(c[0] * d[1] - d[0] * c[1])
        D = float(A0 * B1 - A1 * B0)
        if D != 0:
            x = float((B0 * C1 - B1 * C0) / D)
            y = float((A1 * C0 - A0 * C1) / D)
        else:
            d[0] = d[0] + 0.001
            d[1] = d[1] + 0.001
            A0 = float(a[1] - b[1])
            B0 = float(b[0] - a[0])
            C0 = float(a[0] * b[1] - b[0] * a[1])
            A1 = float(c[1] - d[1])
            B1 = float(d[0] - c[0])
            C1 = float(c[0] * d[1] - d[0] * c[1])
            D = float(A0 * B1 - A1 * B0)
            x = float((B0 * C1 - B1 * C0) / D)
            y = float((A1 * C0 - A0 * C1) / D)
        return x, y

    def LineGen(self, point1, point2, point3, l):
        '''
        已知多边形一条边上两点以及多边形内一点，得到平移后的直线上的两点
        :param point1: 多边形顶点1
        :param point2: 多边形顶点2
        :param point3: 多边形内一点
        :param l: 平移距离
        :return: 平移后直线上两点坐标 list(float,float)*2
        '''
        k = float
        x = float
        y = float
        a = point1
        b = point2
        c = point3
        if b[1] - a[1] != 0 and b[0] - a[0] != 0:
            k = (b[1] - a[1]) / (b[0] - a[0])
            k_1 = -1 / k
            d = [c[0] + 1, c[1] + k_1]
            x, y = self.node_inter(a, b, c, d)
        elif b[0] - a[0] == 0:
            x = float(a[0])
            y = float(c[1])
        elif b[1] - a[1] == 0:
            x = float(c[0])
            y = float(b[1])
        l_len = np.sqrt(np.square(x - c[0]) + np.square(y - c[1]))
        v = [(x - c[0]) / l_len, (y - c[1]) / l_len]
        x_out = x + v[0] * l
        y_out = y + v[1] * l
        if b[1] - a[1] != 0 and b[0] - a[0] != 0:
            return [x_out, y_out], [x_out + 1, y_out + k]
        elif b[0] - a[0] == 0:
            return [x_out, y_out], [x_out, y_out + 1]
        elif b[1] - a[1] == 0:
            return [x_out, y_out], [x_out + 1, y_out]

    def PolygonOutput(self):
        '''
        得到延伸后的多边形的2d顶点坐标
        :return: 两个list，分别为各个顶点的x坐标、y坐标
        '''
        vertex = self.vertex
        n = len(vertex[:, 0])
        l = self.distance
        x_sum = 0
        y_sum = 0
        for item in vertex[:, 0]:
            x_sum += item
        for item in vertex[:, 1]:
            y_sum += item
        x_aver = float(x_sum) / n
        y_aver = float(y_sum) / n
        x = []
        y = []
        a, b = self.LineGen(vertex[n - 1], vertex[0], [x_aver, y_aver], l[3])
        c, d = self.LineGen(vertex[0], vertex[1], [x_aver, y_aver], l[0])
        x_tem, y_tem = self.node_inter(a, b, c, d)
        x.append(x_tem)
        y.append(y_tem)
        a, b = self.LineGen(vertex[0], vertex[1], [x_aver, y_aver], l[0])
        c, d = self.LineGen(vertex[1], vertex[2], [x_aver, y_aver], l[1])
        x_tem, y_tem = self.node_inter(a, b, c, d)
        x.append(x_tem)
        y.append(y_tem)
        if n > 4:
            a, b = self.LineGen(vertex[1], vertex[2], [x_aver, y_aver], l[1])
            c, d = self.LineGen(vertex[2], vertex[3], [x_aver, y_aver], l[1])
            x_tem, y_tem = self.node_inter(a, b, c, d)
            x.append(x_tem)
            y.append(y_tem)
            if n > 5:
                a, b = self.LineGen(vertex[2], vertex[3], [x_aver, y_aver], l[1])
                c, d = self.LineGen(vertex[3], vertex[4], [x_aver, y_aver], l[1])
                x_tem, y_tem = self.node_inter(a, b, c, d)
                x.append(x_tem)
                y.append(y_tem)
        a, b = self.LineGen(vertex[n-3], vertex[n-2], [x_aver, y_aver], l[1])
        c, d = self.LineGen(vertex[n-2], vertex[n-1], [x_aver, y_aver], l[2])
        x_tem, y_tem = self.node_inter(a, b, c, d)
        x.append(x_tem)
        y.append(y_tem)
        a, b = self.LineGen(vertex[n-2], vertex[n-1], [x_aver, y_aver], l[2])
        c, d = self.LineGen(vertex[n-1], vertex[0], [x_aver, y_aver], l[3])
        x_tem, y_tem = self.node_inter(a, b, c, d)
        x.append(x_tem)
        y.append(y_tem)

        return x, y



