import numpy as np

points = np.array([[0.7426, -0.6204, 0.8785],
                   [0.8450, -0.5064, 0.4961],
                   [0.8457, -0.1384, 0.4935],
                   [0.7212, -0.6204, 0.9585],
                   [0.7071, -0.1726, 1.0111]])
A = (points[1][1] - points[0][1]) * (points[2][2] - points[0][2]) - (points[1][2] - points[0][2]) * (
        points[2][1] - points[0][1])
B = (points[2][0] - points[0][0]) * (points[1][2] - points[0][2]) - (points[1][0] - points[0][0]) * (
        points[2][2] - points[0][2])
C = (points[1][0] - points[0][0]) * (points[2][1] - points[0][1]) - (points[2][0] - points[0][0]) * (
        points[1][1] - points[0][1])
D = -(A * points[0][0] + B * points[0][1] + C * points[0][2])
# A * points[0][0] + B * points[0][1] + C * points[0][2] + D = 0
print((- D - B * points[4][1] - C * points[4][2]) / A)
