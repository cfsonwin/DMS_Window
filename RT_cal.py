

import configparser

import numpy as np
config = configparser.ConfigParser()
config.read("./config/random_coor.ini")
point_A = config['Coor_After']
P_a_set = []
keys_count = int(len(config.options('Coor_After')) / 3)
for i in range(keys_count):
    k1 = 'p' + str(i) + 'x'
    k2 = 'p' + str(i) + 'y'
    k3 = 'p' + str(i) + 'z'
    x = float(point_A[k1])
    y = float(point_A[k2])
    z = float(point_A[k3])
    point = [x, y, z]
    P_a_set.append(point)
point_B = config['Coor_Before']
P_b_set = []
keys_count = int(len(config.options('Coor_Before')) / 3)
for i in range(keys_count):
    k1 = 'p' + str(i) + 'x'
    k2 = 'p' + str(i) + 'y'
    k3 = 'p' + str(i) + 'z'
    x = float(point_B[k1])
    y = float(point_B[k2])
    z = float(point_B[k3])
    point = [x, y, z]
    P_b_set.append(point)
M = np.array([P_a_set[0], P_a_set[1], P_a_set[2]])
N = np.array([P_a_set[1], P_a_set[2], P_a_set[3]])
O = M - N
# print(M)
# print(N)
# print(O)
M_1 = np.linalg.inv(O)
l1 = np.array([[P_b_set[0][0]], [P_b_set[1][0]], [P_b_set[2][0]]])
l2 = np.array([[P_b_set[0][1]], [P_b_set[1][1]], [P_b_set[2][1]]])
l3 = np.array([[P_b_set[0][2]], [P_b_set[1][2]], [P_b_set[2][2]]])

l1_ = np.array([[P_b_set[1][0]], [P_b_set[2][0]], [P_b_set[3][0]]])
l2_ = np.array([[P_b_set[1][1]], [P_b_set[2][1]], [P_b_set[3][1]]])
l3_ = np.array([[P_b_set[1][2]], [P_b_set[2][2]], [P_b_set[3][2]]])

l11 = l1 - l1_
l22 = l2 - l2_
l33 = l3 - l3_

# print(M_1)
# print(l1)
l111 = M_1.dot(l11)
l222 = M_1.dot(l22)
l333 = M_1.dot(l33)
# print(l111)
# print(l222)
# print(l333)
R = np.array([[float(l111[0]), float(l111[1]), float(l111[2])],
              [float(l222[0]), float(l222[1]), float(l222[2])],
              [float(l333[0]), float(l333[1]), float(l333[2])]])
# R_1, T_1 = f0()
T = P_b_set[0] - R.dot(P_a_set[0])
print(R)
print(T)