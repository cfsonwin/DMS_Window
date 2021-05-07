import configparser
import numpy as np
class Read_Region_Info:
    def __init__(self, car_name):
        self.filename = r'./config/' + car_name + r'_coor_info.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)
        # for key in self.config['car_Info']:
        #     print(key)
        self.car_name = self.config['car_Info']['car_name']
        self.region_num = int(self.config['car_Info']['region_num'])
        self.extend_init = float(self.config['car_Info']['extend_init'])

    def ReadData(self):
        edges = []
        for i in range(0, self.region_num):
            section_name = self.car_name + '_Region_' + chr(65 + i)
            # print(section_name)
            points = []
            for j in range(0, int(self.config[section_name]['edge_point'])):
                p_x = float(self.config[section_name]['p' + str(j) + 'x'])
                p_y = float(self.config[section_name]['p' + str(j) + 'y'])
                p_z = float(self.config[section_name]['p' + str(j) + 'z'])
                point = [p_x, p_y, p_z]
                points.append(point)
            edges.append(points)
        # print(edges)
        Info = np.array()
        return np.array(edges)
    def WriteData(self):
        pass


if __name__ == '__main__':
    region_info = Read_Region_Info('vx1')
    region = region_info.ReadData()
    print(region)
