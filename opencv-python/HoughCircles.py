import cv2 as cv
import os
import time
import numpy as np
import matplotlib.pyplot as plt


# 专用去重
def drop_list(LList):
    LList = LList.tolist()
    new_LList = []
    for x in LList:
        if x not in new_LList:
            new_LList.append(x)
    return np.array(new_LList)


# 找出分组中最大的圆
def find_max(group1):
    group1 = np.array(group1)
    Radius = []
    for x in group1:
        Radius.append(x[2])
    Max = np.max(Radius)
    for x in group1:
        if x[2] == Max:
            return x


# 计算两个圆心之间的距离
def calculate_center(x1, y1, x2, y2):
    zw = np.square((x1 - x2)) + np.square((y1 - y2))
    zw = np.sqrt(zw)
    return zw


# 灰度图的直方图
def hist(image):
    hist = cv.calcHist([image], [0], None, [256], [0.0, 255.0])
    plt.figure()
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()


# 检测每个洞外围最大的圆
# 返回整个图像 和 每个圆的数据（圆心坐标，半径 单位是像素块）
def OUTSIDE_detect_circles(image):
    '''
    图像预处理
    '''
    start = time.time()
    dst = cv.pyrMeanShiftFiltering(image, 30, 100)
    print('cost:{:0.2f}s'.format(time.time() - start))
    dst = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    dst = cv.bilateralFilter(dst, 0, 40, 10, 4)
    circles = cv.HoughCircles(dst, cv.HOUGH_GRADIENT, 1, 20,
                              param1=50, param2=20,
                              minRadius=0, maxRadius=0)
    if circles is None:
        return None, None
    circles = circles[0, :]
    '''
    每张图N个洞，分N个组，计算每个组最大的圆
    '''
    result = []
    circles_numbers = len(circles)
    print(circles)
    print('-----------------------------------------------------')
    for c in range(circles_numbers):
        group = []
        flag = 0
        for c2 in range(circles_numbers):
            if c != c2:
                distance = calculate_center(circles[c][0], circles[c][1],
                                            circles[c2][0], circles[c2][1])
                R = circles[c][2] + circles[c2][2]
                if 0 < distance < R:
                    group.append(circles[c])
                    group.append(circles[c2])
                    flag = flag + 1
        if flag == 0:
            result.append(circles[c])
            print('独狼', circles[c])
        if group:
            print('每次的分组', np.array(group))
            MAX_RADIUS_CIRCLE = find_max(group)
            print('最大的圆', MAX_RADIUS_CIRCLE)
            result.append(MAX_RADIUS_CIRCLE)
    '''
    去重
    '''
    result = np.array(result)
    result = drop_list(result)
    '''
    取整，像素点没有小数。
    这会出现较大的精测误差
    '''
    result = np.uint16(np.around(result))
    print('result=', result)
    for i in result:
        cv.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 2)  # 画圆
        cv.circle(image, (i[0], i[1]), 2, (255, 0, 0), 2)  # 圆心
    return result, image


'''
1. 截出大圆
2. 检测小圆，绘制
3. 将截图放回大图，并打上序列标签
4. 根据序列标签输入小圆真实半径
5. 计算误差并绘制
误差(单位：毫米mm) = 小圆真实直径 X (大圆像素直径 - 小圆像素直径) / 小圆像素直径
'''


# 此函数完成1~3步骤
def GO_AND_BACK(OUTSIDE_CIRCLE_DATA, IMAGE):
    # 存放小圆的直径
    result = []
    for data in OUTSIDE_CIRCLE_DATA:
        x = data[0]
        y = data[1]
        Radius = data[2]
        x = x - Radius
        y = y - Radius
        d = 2 * Radius
        RECT_circle = IMAGE[y:y+d, x:x+d]
        cv.imshow('', RECT_circle)
        cv.waitKey()
        hist(RECT_circle)





if __name__ == '__main__':
    for x, y, z in os.walk(r'D:\resource_AI\A'):
        for name in z:
            filepath = r'D:\resource_AI\A\{}'.format(name)
            img = cv.imread(filepath)
            OUTSIDE_circle_data, dst = OUTSIDE_detect_circles(img)
            cv.namedWindow('', 0)
            cv.resizeWindow('', 1600, 800)
            cv.imshow('', dst)
            cv.waitKey()

            GO_AND_BACK(OUTSIDE_circle_data, dst)

