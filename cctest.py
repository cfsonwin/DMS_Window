import configparser

import numpy as np


def f0():
    v1 = np.array([0.28, 0.33, 1])
    v2 = np.array([-0.2, -0.44, 0.23])
    vn = np.cross(v1, v2)
    # print(vn)
    v2 = np.cross(v1, vn)
    # print(v2)
    R = np.array([v1, v2, vn]).T
    # print(R)
    T = np.array([[0.1], [0.2], [0.3]])
    a1 = np.array([[1], [0], [0]])
    a2 = np.array([[0], [1], [0]])
    a3 = np.array([[0], [0], [1]])
    b1 = T + R.dot(a1)
    b2 = T + R.dot(a2)
    b3 = T + R.dot(a3)
    return R, T


def f1():
    config = configparser.ConfigParser()
    config.read("./config/random_coor.ini")
    points_test_F = np.random.randint(100, size=(5, 3))
    config.add_section('Coor_After')
    for i in range(len(points_test_F)):
        k0 = 'p' + str(i) + 'x'
        k1 = 'p' + str(i) + 'y'
        k2 = 'p' + str(i) + 'z'
        config.set('Coor_After', k0, str(points_test_F[i][0] / 10))
        config.set('Coor_After', k1, str(points_test_F[i][1] / 10))
        config.set('Coor_After', k2, str(points_test_F[i][2] / 10))
    config.write(open("./config/random_coor.ini", "w"))
    config.add_section('Coor_Before')
    R, T = f0()
    for i in range(len(points_test_F)):
        k0 = 'p' + str(i) + 'x'
        k1 = 'p' + str(i) + 'y'
        k2 = 'p' + str(i) + 'z'
        vec = points_test_F[i] / 10
        print('vec: ', vec)
        vec = T + R.dot(vec.reshape([3, 1]))
        print('vec now: ', vec)
        config.set('Coor_Before', k0, str(vec[0][0]))
        config.set('Coor_Before', k1, str(vec[1][0]))
        config.set('Coor_Before', k2, str(vec[2][0]))
    config.write(open("./config/random_coor.ini", "w"))


def f2():
    # R, T = f0()
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
        # print(point)
    P_a_set = np.mat(P_a_set)
    # print(P_a_set)
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
        # print(point)
    P_b_set = np.mat(P_b_set)
    # print(P_b_set)
    return P_a_set, P_b_set


def f3():
    P_a_set, P_b_set = f2()
    R, T = f0()
    print(R)

    # for i in range(5):
    #     print(T + R.dot(P_a_set[i].reshape([3, 1])) - P_b_set[i].reshape([3, 1]))
    centorid_B = (P_b_set[0] + P_b_set[1] + P_b_set[2] + P_b_set[3] + P_b_set[4]) / 5
    centorid_A = (P_a_set[0] + P_a_set[1] + P_a_set[2] + P_a_set[3] + P_a_set[4]) / 5
    # centorid_B = (P_b_set[0] + P_b_set[1] + P_b_set[2]) / 3
    # centorid_A = (P_a_set[0] + P_a_set[1] + P_a_set[2]) / 3
    H = np.mat([[0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]])
    ma = []
    mb = []
    for k in range(0, 5):
        m1 = []
        m2 = []
        mar1 = P_a_set[k] - centorid_B
        mar2 = P_b_set[k] - centorid_A
        mar3 = mar2.T
        H += np.dot(mar3, mar1)
        mar1 = mar1.T
        mar2 = mar2.T
        for i in range(0, 3):
            m1.append(float(mar1[i]))
            m2.append(float(mar2[i]))
        ma.append(m1)
        mb.append(m2)

    # print('H: ', H)
    ma = np.array(ma)
    mb = np.array(mb)
    ma = ma.T
    mc = ma.dot(mb)
    print(mc)
    U, s, V = np.linalg.svd(mc)
    print('U: ', U)
    print('s: ', s)
    print('V: ', V)
    Ut = U
    Vt = V
    det = np.linalg.det(U.dot(V))
    # print('Ut: ', Ut)
    M = np.mat([[1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, det]])
    M1 = np.dot(Vt, M)
    R = np.dot(M1, Ut)
    t = centorid_B.T - np.dot(R, centorid_A.T)

    print('R: ', R)
    print('t: ', t)


def f4():
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
    # print(R_1)



f4()
