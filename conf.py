#
# import os
# print(os.path.dirname(__file__))
# print ('***获取当前目录***')
# print (os.getcwd())
# print (os.path.abspath(os.path.dirname(__file__)))
# # __file__ 为当前文件, 若果在ide中运行此行会报错,可改为  #d = path.dirname('.')
# # 但是改为.后，就是获得当前目录，接着使用dirname函数访问上级目录
# print ('***获取上级目录***')
# print (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
# print (os.path.abspath(os.path.dirname(os.getcwd())))
# print (os.path.abspath(os.path.join(os.getcwd(), "..")))
#
# print ('***获取上上级目录***')
# print (os.path.abspath(os.path.join(os.getcwd(), "../..")))
#
# conf_path = os.path.dirname(__file__) + r'/config/Coor_info.ini'
# print(conf_path)
import configparser
import numpy as np
config = configparser.ConfigParser()
# print("- Empty config %s"%config.sections())

# print("- Load config file")
config.read("./config/Coor_info.ini")
# points = config['vx1']
# regioninfo = []
# keys_count = int(len(config.options('vx1'))/3)
# for i in range(keys_count):
#     k1 = 'p' + str(i) + 'x'
#     k2 = 'p' + str(i) + 'y'
#     k3 = 'p' + str(i) + 'z'
#     x = float(points[k1])
#     y = float(points[k2])
#     z = float(points[k3])
#     point = [x, y, z]
#     regioninfo.append(point)
#     # print(point)
# regioninfo = np.array(regioninfo)
# print(regioninfo)

def 将三维坐标信息录入配置文件():
    config = configparser.ConfigParser()
    config.read("./config/Coor_info.ini")
    points_test_F = np.array([[-0.995596, -0.470681, 0.679959],
                              [-0.995596, -0.470681, -0.320041],
                              [-0.395596, -0.470681, -0.320041],
                              [-0.395596, -0.470681, 0.179959],
                              [0.325404, -0.470681, 0.179959],
                              [0.325404, -0.470681, 0.679959]])
    config.add_section('vx1_Region_F')
    for i in range(len(points_test_F)):
        k0 = 'p' + str(i) + 'x'
        k1 = 'p' + str(i) + 'y'
        k2 = 'p' + str(i) + 'z'
        config.set('vx1_Region_F', k0, str(points_test_F[i][0]))
        config.set('vx1_Region_F', k1, str(points_test_F[i][1]))
        config.set('vx1_Region_F', k2, str(points_test_F[i][2]))
    config.write(open("./config/Coor_info.ini", "w"))


'''
1.读取配置文件
- read(filename) 直接读取ini文件内容
- sections() 得到所有的section，并以列表的形式返回
- options(section) 得到该section的所有option
- items(section) 得到该section的所有键值对
- get(section,option) 得到section中option的值，返回为string类型
- getint(section,option) 得到section中option的值，返回为int类型

2.写入配置文件
- add_section(section) 添加一个新的section
- set( section, option, value) 对section中的option进行设置
需要调用write将内容写入配置文件
'''
## 此处返回的sections list不包括 default
# print("> config sections : %s"%config.sections())
# print('bitbucket.org' in config )  ## 判断配置文件中是否存在该 section
# print("> Load config file is :")

# for section in config.keys():
#     print("[{s}]".format(s=section))
#     for key in config[section]:
#         print("{k} = {v}".format(k=key, v=config[section][key]))
#
# ## 如访问 dict 一样读取配置内容
# print("\n- Get value like dict :user =  %s"%config['bitbucket.org']['user'])
# conf_bitbucket = config['bitbucket.org']
# print(conf_bitbucket['user'])

# """
# The DEFAULT section which provides default values for all other sections"""
# print("\n- DEFAULT Section")
# ## default 是所有section的默认设置，备胎...
# for key in config['bitbucket.org']: print(key)
# print("> Get default value : forwardx11 = %s\n"%config['bitbucket.org']['forwardx11'])
# #
# ## 读取不同数据类型的配置参数
# print("\n- Support datatypes")
# forwardx11 = config['bitbucket.org'].getboolean('forwardx11')
# int_port = config.getint('topsecret.server.com', 'port')
# float_port = config.getfloat('topsecret.server.com', 'port')
# print("> Get int port = %d type : %s"%(int_port, type(int_port)))
# print("> Get float port = %f type : %s"%(float_port, type(float_port)))