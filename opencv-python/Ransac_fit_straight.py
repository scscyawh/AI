import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt
import time

"""
精度优化：
1.直方图的断点判断：目前只会判断最大值，理由判断突变点(导数最大值)。
2.目前使用的拟合方式会受到干扰,干扰程度不一。

运算时间优化：
1.目前运算时间大约在300~400ms。

需要新添的功能：
1.拟合度计算
"""


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
    固定间隙要在中间，
    然后从中间分成左右两边计算
    :param PATH: 图片路径，二值图
    :return: 面差和间隙和图像
    """
    start_time = time.time()
    img = cv.imread(PATH)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_height = img_gray.shape[0]
    img_weight = img_gray.shape[1]
    clip_point = int(img_weight / 2)

    # 准备数据
    point_right = []
    point_left = []
    all_points = []
    for weight in range(img_gray.shape[1]):
        for hight in range(img_gray.shape[0]):
            if img_gray[hight, weight] > 50:
                all_points.append([weight, hight])
                if weight < clip_point:
                    point_left.append([weight, hight])
                else:
                    point_right.append([weight, hight])
    point_left = np.array(point_left)
    point_right = np.array(point_right)
    all_points = np.array(all_points)

    # 开始拟合
    output_left = cv.fitLine(point_left, cv.DIST_L1, 0, 0.01, 0.01)
    output_rihgt = cv.fitLine(point_right, cv.DIST_L1, 0, 0.01, 0.01)
    left_k, left_b = find_kb(output_left[0], output_left[1], output_left[2], output_left[3])
    right_k, right_b = find_kb(output_rihgt[0], output_rihgt[1], output_rihgt[2], output_rihgt[3])

    # 画线
    left_Y = left_k * clip_point + left_b
    cv.line(img, (0, left_b), (clip_point, int(left_Y)), (0, 0, 255), 1)

    rihgt_Y_start = right_k * clip_point + right_b
    rihgt_Y = right_k * img_gray.shape[1] + right_b
    cv.line(img, (clip_point, int(rihgt_Y_start)), (img_gray.shape[1], int(rihgt_Y)), (0, 255, 0), 1)

    # 画直方图（x为横坐标、y为拟合直线y值与白色像素点y值的差值）
    hist_left_x = []
    hist_left_y = []

    hist_right_x = []
    hist_right_y = []
    for one_point in all_points:
        if one_point[0] < clip_point:  # 左图
            hist_left_x.append(one_point[0])
            line_y = left_k * one_point[0] + left_b
            result_y = abs(line_y - one_point[1])
            hist_left_y.append(result_y)
        else:
            hist_right_x.append(one_point[0])
            line_y = right_k * one_point[0] + right_b
            result_y = abs(line_y - one_point[1])
            hist_right_y.append(result_y)
    hist_left_y = np.array(hist_left_y)
    hist_right_y = np.array(hist_right_y)

    # 寻找断点
    left_VIP = hist_left_x[np.argmax(hist_left_y)]
    right_VIP = hist_right_x[np.argmax(hist_right_y)]
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, '|{}'.format(left_VIP), (left_VIP, all_points[left_VIP][1]), font,
               1, (0, 0, 255), 1)
    cv.putText(img, '|{}'.format(right_VIP), (right_VIP, all_points[right_VIP][1]), font,
               1, (0, 255, 0), 1)

    # 计算间隙
    clearance_error = right_VIP - left_VIP
    cv.putText(img, 'clearance error is {} px'.format(clearance_error),
               (right_VIP - 250, all_points[right_VIP][1] - 50), font,
               1, (255, 0, 0), 1)

    # 计算面差
    fin_re = 0
    cont = 0
    for r in range(left_VIP, right_VIP + 1):
        dimension_left = left_k * r + left_b
        dimension_right = right_k * r + right_b
        re = abs(dimension_left - dimension_right)
        fin_re = fin_re + re
        cont = cont + 1
    dimension = float(fin_re / cont)
    dimension_error = np.around(dimension, 2)
    cv.putText(img, 'dimension error is {} px'.format(dimension_error),
               (right_VIP - 250, all_points[right_VIP][1] + 100), font,
               1, (255, 0, 0), 1)

    print('cost:{:0.2f}ms'.format((time.time() - start_time) * 1000))
    # 完工
    cv.namedWindow('', 0)
    cv.resizeWindow('', 1600, 1000)
    cv.imwrite('123.png', img)
    cv.imshow('', img)
    plt.subplot(121)
    plt.title('left')
    plt.xlabel('x')
    plt.ylabel('the calculation of y')
    plt.plot(hist_left_x, hist_left_y)
    plt.subplot(122)
    plt.title('right')
    plt.xlabel('x')
    plt.ylabel('the calculation of y')
    plt.plot(hist_right_x, hist_right_y)
    plt.show()
    cv.waitKey()
    return clearance_error, dimension_error, img


if __name__ == '__main__':
    for x, y, z in os.walk(r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA'):
        for filename in z:
            print('-----------------------------------------------')
            path = r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA\{}'.format(filename)
            c_e, d_e, i = ransc(path)
