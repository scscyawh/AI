import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt
import time

p_left_ = -10
p_right_ = -5
a_left_ = -10
a_right = -5
"""
运算时间优化：
1.目前运算时间大约在300~400ms。

需要新添的功能：
1.拟合度计算
"""


def draw_start_end_point(start_p, end_p, img, color=None):
    if color is None:
        color = [0, 0, 255]
    for flag in range(0, 26):
        img[start_p[1] - 13 + flag, start_p[0]] = color
        img[end_p[1] - 13 + flag, end_p[0]] = color
    return img


def find_kb(x1, x2, x3, x4):
    """
    计算cv.line返回的点斜氏方程数据的k、b值
    :param x1:
    :param x2:
    :param x3:
    :param x4:
    :return:
    """
    k = x2 / x1
    b = x4 - (k * x3)
    return k, b


def ransc(PATH):
    """
    1. 首次大致寻找间断点,点与点之间的距离
    2. 根据间断点分区拟合直线
    3. 再一次寻找间断点，点与直线之间的距离
    4. 计算
    :param PATH: 图片路径，二值图
    :return: 面差和间隙和图像
    """
    global start_point, end_point
    font = cv.FONT_HERSHEY_SIMPLEX
    img = cv.imread(PATH)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_height = img_gray.shape[0]
    img_weight = img_gray.shape[1]

    # 准备数据
    all_points = []  # 所有的坐标点
    start_time = time.time()
    for weight in range(img_weight):
        for hight in range(img_height):
            if img_gray[hight, weight] > 50:
                all_points.append([weight, hight])
    print('cost---:{}ms'.format((time.time() - start_time) * 1000))
    all_points = np.array(all_points)

    # 寻找大致断点,点与点之间
    for p_i in range(len(all_points) - 1):
        flag = all_points[p_i][1] - all_points[p_i + 1][1]
        if flag < p_left_:
            start_point = all_points[p_i]
            print(start_point)
            break
    for p_i in reversed(range(1, len(all_points))):
        flag = all_points[p_i][1] - all_points[p_i - 1][1]
        if flag < p_right_:
            end_point = all_points[p_i]
            print(end_point)
            break
    if (start_point is None) or (end_point is None) or (start_point[0] > end_point[0]):
        print('error')
        exit(0)
    draw_start_end_point(start_point, end_point, img)

    # 断点外的精确拟合
    point_left = []
    point_right = []
    for fit_point in all_points:
        if fit_point[0] < start_point[0]:
            point_left.append(fit_point)
        if fit_point[0] > end_point[0]:
            point_right.append(fit_point)
    point_left = np.array(point_left)
    point_right = np.array(point_right)
    # 开始拟合
    output_left = cv.fitLine(point_left, cv.DIST_L1, 0, 0.01, 0.01)
    output_rihgt = cv.fitLine(point_right, cv.DIST_L1, 0, 0.01, 0.01)
    # 计算k、b
    left_k, left_b = find_kb(output_left[0], output_left[1], output_left[2], output_left[3])
    right_k, right_b = find_kb(output_rihgt[0], output_rihgt[1], output_rihgt[2], output_rihgt[3])
    # 绘直线
    left_Y = left_k * start_point[0] + left_b
    cv.line(img, (0, left_b), (start_point[0], int(left_Y)), (0, 0, 255), 1)
    rihgt_Y_start = right_k * end_point[0] + right_b
    rihgt_Y = right_k * img_gray.shape[1] + right_b
    cv.line(img, (end_point[0], int(rihgt_Y_start)), (img_gray.shape[1], int(rihgt_Y)), (0, 255, 0), 1)

    # 寻找精确断点，点与直线之间
    for a_p in all_points:
        flag = np.around(((left_k * a_p[0] + left_b) - a_p[1]), 0)
        if flag < a_left_:
            start_point = a_p
            break
    for a_p in reversed(all_points):
        flag = np.around(((right_k * a_p[0] + right_b) - a_p[1]), 0)
        if flag < a_right:
            end_point = a_p
            break
    draw_start_end_point(start_point, end_point, img, color=[0, 215, 255])

    # 计算面差与间隙
    x1 = start_point[0]
    y1 = left_k * x1 + left_b
    x2 = end_point[0]
    y2 = right_k * x2 + right_b
    dimension_error = float(abs(y2 - y1))
    clearance_error = int(abs(x2 - x1))
    cv.putText(img, 'dimension error is {:0.3f}px'.format(dimension_error),
               (x1-150, y1 - 100), font, 1, (255, 255, 255), 1)
    cv.putText(img, 'clearance error is {}px'.format(clearance_error),
               (x1-150, y1 + 100), font, 1, (255, 255, 255), 1)

    cv.namedWindow('', 0)
    cv.resizeWindow('', 1600, 1000)
    cv.imwrite('123.png', img)
    cv.imshow('', img)
    cv.waitKey()
    return dimension_error, clearance_error, img


if __name__ == '__main__':
    for x, y, z in os.walk(r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA'):
        for filename in z:
            path = r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA\{}'.format(filename)
            print('--------------------{}---------------------------'.format(path))
            d_r, c_r, i = ransc(path)


