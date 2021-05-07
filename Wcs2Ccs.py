import numpy as np
def f0(tilt, tele):
    a = '8000'
    b = '8271'
    c = '820a'
    a_int = int(a, 16)
    b_int = int(b, 16)
    c_int = int(c, 16)
    tilt_int = int(tilt, 16)
    tele_int = int(tele, 16)
    theta = round((tilt_int - a_int) / (c_int - a_int) * (25.28 - 20.22) + 20.22, 5)
    delta = round((tele_int - a_int) / (b_int - a_int) * 60, 5)
    # print(theta, '\n', delta)
    return theta, delta



def Ccs2Wcs(tilt, tele):
    # 20.22°~25.78°
    # theta = 20.22
    theta, d = f0(tilt, tele)
    P_inCcs = np.array([[0],
                      [0.5],
                      [1]])
    V_inCcs = np.array([[0],
                        [0],
                        [-1]])
    T_ba = np.array([[0],
                     [-38.196],
                     [389.901 + d]])

    P_inA = P_inCcs + T_ba

    # 20.22°~25.78°
    #theta = 20.22
    sin = np.sin(np.radians(theta))
    cos = np.cos(np.radians(theta))
    R = np.array([[0, sin, cos],
                  [-1, 0, 0],
                  [0, -cos, sin]])
    T_ao = np.array([[495.841],
                     [-390],
                     [674.646]])

    P_inO = R.dot(P_inA) + T_ao

    # print(R)
    print(P_inO / 1000)
    print(R.dot(V_inCcs))

tilt = '813b'
tele = '8152'
Ccs2Wcs(tilt, tele)