import cv2 as cv
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from xlutils.copy import copy
import xlrd

from tkinter import *
import tkinter.messagebox


def save_excel(row, col, value, path):
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.col(col).width = 200 * 100
    ws.write(row, col, value)
    wb.save(path)


def zhuanyong_INT(number):
    """
    专用取整函数
    :param number:
    :return:
    """
    re_x = int(np.around(number, 0))
    return re_x


def getInput(title, message):
    """
    输入框，并返回输入值
    :param title: 标题
    :param message: 提示信息
    :return: 返回输入值，类型str
    """

    def return_callback(event):
        root.quit()

    def close_callback():
        tkinter.messagebox.showinfo('提示', '确定退出？')
        str = None
        root.quit()

    root = Tk(className=title)
    root.wm_attributes('-topmost', 1)
    screenwidth, screenheight = root.maxsize()
    width = 300
    height = 100
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
    root.resizable(0, 0)
    lable = Label(root, height=2)
    lable['text'] = message
    lable.pack()
    entry = Entry(root)
    entry.bind('<Return>', return_callback)
    entry.pack()
    entry.focus_set()
    root.protocol("WM_DELETE_WINDOW", close_callback)
    root.mainloop()
    str = entry.get()
    root.destroy()
    return str


def drop_list(LList):
    """
    二维列表去重
    :param LList:
    :return:
    """
    LList = LList.tolist()
    new_LList = []
    for x in LList:
        if x not in new_LList:
            new_LList.append(x)
    return np.array(new_LList)


def find_max(group1):
    """
    找出一组中最大的圆
    :param group1: 一组圆（坐标和半径）
    :return:
    """
    group1 = np.array(group1)
    Radius = []
    for x in group1:
        Radius.append(x[2])
    Max = np.max(Radius)
    for x in group1:
        if x[2] == Max:
            return x


def calculate_center(x1, y1, x2, y2):
    """
    计算两坐标的像素距离
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    zw = np.square((x1 - x2)) + np.square((y1 - y2))
    zw = np.sqrt(zw)
    return zw


def hist(image):
    """
    直方图
    :param image:
    :return:
    """
    hist = cv.calcHist([image], [0], None, [256], [0.0, 255.0])
    # plt.figure()
    # plt.plot(hist)
    # plt.xlim([0, 256])
    # plt.show()
    return hist


def OUTSIDE_detect_circles(image):
    """
    检测原图中每个洞的最大圆，返回每个圆的数据
    :param image: 原图
    :return: 只需要返回每个大圆的数据，cv.circle是直接在原图上绘图的
    """
    # 图像预处理
    start = time.time()
    dst_py = cv.pyrMeanShiftFiltering(image, 30, 100)
    print('pyrMeanShiftFiltering_cost:{:0.2f}s'.format(time.time() - start))
    dst_GRAY = cv.cvtColor(dst_py, cv.COLOR_BGR2GRAY)
    dst = cv.bilateralFilter(dst_GRAY, 0, 40, 10, 4)
    '''
    cv.namedWindow('', 0)
    cv.resizeWindow('', 1600, 800)
    cv.imshow('', cv.Canny(dst, 25, 50))
    cv.waitKey()
    '''

    # 霍夫变换圆检测
    circles = cv.HoughCircles(dst, cv.HOUGH_GRADIENT, 1, 20,
                              param1=50, param2=18,
                              minRadius=0, maxRadius=0)
    image_weight = dst.shape[1]
    image_hight = dst.shape[0]
    if circles is None:
        print('第一阶段未检测到圆')
        return None
    circles = circles[0, :]

    # 每张图N个洞，分N个组，计算每个组最大的圆
    result = []
    circles_numbers = len(circles)
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
            result.append(circles[c])  # 独狼情况
        if group:
            MAX_RADIUS_CIRCLE = find_max(group)
            result.append(MAX_RADIUS_CIRCLE)

    # 去重
    result = np.array(result)
    result = drop_list(result)

    # 去除圆的形状超过图片分辨率的圆
    beyond_result = []
    for circle_beyond in result:
        beyond_x = circle_beyond[0]
        beyond_y = circle_beyond[1]
        beyond_r = circle_beyond[2]
        top = beyond_y - beyond_r
        bottom = beyond_y + beyond_r
        right = beyond_x + beyond_r
        left = beyond_x - beyond_r
        if top > 0 and bottom < image_hight and right < image_weight and left > 0:
            beyond_result.append(circle_beyond)
    beyond_result = np.array(beyond_result)

    # 计算圆的拟合程度
    matching_result = []
    for circle_matching in beyond_result:
        # 先将圆截出来，减小计算量
        dst_Canny = cv.Canny(dst, 25, 50)
        matching_x = circle_matching[0]
        matching_y = circle_matching[1]
        matching_r = circle_matching[2]
        y_clip = zhuanyong_INT(matching_y) - zhuanyong_INT(matching_r) - 10
        if y_clip < 0:
            y_clip = 0
        x_clip = zhuanyong_INT(matching_x) - zhuanyong_INT(matching_r) - 10
        if x_clip < 0:
            x_clip = 0
        matching_image = dst_Canny[y_clip:zhuanyong_INT(matching_y) + zhuanyong_INT(matching_r) + 10,
                                   x_clip:zhuanyong_INT(matching_x) + zhuanyong_INT(matching_r) + 10]
        # 开始计算：将霍夫检测得到的圆映射到Canny图中，计算圆边上的白色像素块的占比。
        all_points = 0
        in_circle_points = 0
        for weigh in range(matching_image.shape[1]):
            for high in range(matching_image.shape[0]):
                if zhuanyong_INT(
                        calculate_center(weigh, high, matching_x - x_clip, matching_y - y_clip)) == zhuanyong_INT(
                                         matching_r):
                    all_points = all_points + 1
                    if matching_image[high, weigh] == 255:
                        in_circle_points = in_circle_points + 1

        matching_result_data = (in_circle_points / all_points) * 100
        print('大圆的拟合程度为:{:0.2f}%'.format(matching_result_data))

        if matching_result_data > 10:
            matching_result.append(circle_matching)
            cv.rectangle(image, (zhuanyong_INT(matching_x - matching_r), zhuanyong_INT(matching_y - matching_r)),
                         (zhuanyong_INT(matching_x + matching_r), zhuanyong_INT(matching_y + matching_r)),
                         (0, 255, 0), 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(image, "{:0.2f}%".format(matching_result_data),
                       (zhuanyong_INT(matching_x - matching_r * 2), zhuanyong_INT(matching_y - matching_r)),
                       font, 1, (0, 0, 255), 2)

    # 取整，因为像素点没有小数。
    for i in matching_result:
        cv.circle(image, (zhuanyong_INT(i[0]), zhuanyong_INT(i[1])),
                  zhuanyong_INT(i[2]), (0, 0, 255), 2)  # 画圆
        cv.circle(image, (zhuanyong_INT(i[0]), zhuanyong_INT(i[1])),
                  2, (255, 0, 0), 2)  # 圆心
    '''
    cv.namedWindow('', 0)
    cv.resizeWindow('', 1600, 800)
    cv.imshow('', image)
    cv.waitKey()
    '''
    return matching_result


def INSIDE_DETECT(OUTSIDE_CIRCLE_DATA, IMAGE, SRC_IMAGE):
    """
    用原图图像处理；用已绘制大圆的图绘制小圆

    截出大圆，检测小圆，绘制小圆，将小图放回大图；
    再为每一组圆做好序列标签，字典{key标签:value大圆像素坐标、小圆像素坐标、小圆像素直径}
    :param OUTSIDE_CIRCLE_DATA: 每个大圆的数据
    :param IMAGE: 已绘制大圆的图像
    :param SRC_IMAGE: 原图
    :return: 返回序列标签，字典{};cv.circle是直接在原图上绘图的
    """
    label = 0
    result_data = {}
    # 获取大圆数据
    for data in OUTSIDE_CIRCLE_DATA:
        label = label + 1
        circle_x = data[0]
        circle_y = data[1]
        Radius = data[2]

        # 计算截图范围
        X = circle_x - Radius
        Y = circle_y - Radius
        d = 2 * Radius

        # 有大圆的图（小圆在此图上绘制）
        HAVE_RED_RECT_CIRCLE = IMAGE[zhuanyong_INT(Y):zhuanyong_INT(Y) + zhuanyong_INT(d),
                               zhuanyong_INT(X):zhuanyong_INT(X) + zhuanyong_INT(d)]

        # 对原图（没有画大圆的图进行处理，找小圆）
        RECT_circle = SRC_IMAGE[zhuanyong_INT(Y):zhuanyong_INT(Y) + zhuanyong_INT(d),
                      zhuanyong_INT(X):zhuanyong_INT(X) + zhuanyong_INT(d)]

        # 图像预处理
        RECT_circle = cv.cvtColor(RECT_circle, cv.COLOR_BGR2GRAY)

        # 利用直方图计算二值化的阈值
        points = hist(RECT_circle)
        point_50 = []
        for hist_x in range(len(points)):
            point_50.append(points[hist_x])
            if hist_x > 51:
                break
        bonding = np.argmax(point_50)
        bonding = (50 - bonding) / 2 + bonding

        ret, RECT_circle_THre = cv.threshold(RECT_circle, zhuanyong_INT(bonding),
                                             255, cv.THRESH_BINARY_INV)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        RECT_circle_CLOSE = cv.morphologyEx(RECT_circle_THre, cv.MORPH_CLOSE, kernel)
        RECT_circle_MEDIAN = cv.medianBlur(RECT_circle_CLOSE, 5)
        '''
        cv.namedWindow('', 0)
        cv.resizeWindow('', 1422, 340)
        cv.imshow('', np.hstack([RECT_circle, RECT_circle_THre, RECT_circle_CLOSE, RECT_circle_MEDIAN,
                                 cv.Canny(RECT_circle_MEDIAN, 25, 50)]))
        cv.waitKey(0)
        '''
        INSIDE_CIRCLE = cv.HoughCircles(RECT_circle_MEDIAN, cv.HOUGH_GRADIENT,
                                        1, 10,
                                        param1=50, param2=10, minRadius=0, maxRadius=0)
        if INSIDE_CIRCLE is None:
            print('未找到')
            continue
        INSIDE_CIRCLE = INSIDE_CIRCLE[0, :]
        INSIDE_CIRCLE = find_max(INSIDE_CIRCLE)

        # 计算拟合程度
        circle_canny = cv.Canny(RECT_circle_MEDIAN, 25, 50)
        all_points = 0
        in_points = 0
        for weigh in range(circle_canny.shape[1]):
            for high in range(circle_canny.shape[0]):
                if zhuanyong_INT(calculate_center(weigh, high, INSIDE_CIRCLE[0], INSIDE_CIRCLE[1])) == zhuanyong_INT(
                        INSIDE_CIRCLE[2]):
                    all_points = all_points + 1
                    if circle_canny[high, weigh] == 255:
                        in_points = in_points + 1
        matching = (in_points / all_points) * 100
        print('小圆的拟合程度为:{:0.2f}%'.format(matching))

        if matching > 10:
            # 绘制拟合度
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(IMAGE, '{:0.2f}%'.format(matching),
                       (zhuanyong_INT(circle_x - Radius * 2), zhuanyong_INT(circle_y + Radius + 30)),
                       font, 1, (0, 255, 255), 2)

            # 取整，因为像素点没有小数。
            cv.circle(HAVE_RED_RECT_CIRCLE, (zhuanyong_INT(INSIDE_CIRCLE[0]), zhuanyong_INT(INSIDE_CIRCLE[1])),
                      zhuanyong_INT(INSIDE_CIRCLE[2]), (0, 255, 255), 2)
            cv.circle(HAVE_RED_RECT_CIRCLE, (zhuanyong_INT(INSIDE_CIRCLE[0]), zhuanyong_INT(INSIDE_CIRCLE[1])),
                      1, (0, 255, 255), 2)

            # 序列:字典{key标签:value大圆像素坐标、小圆像素坐标、小圆像素直径}
            result_data[label] = (circle_x, circle_y,
                                  INSIDE_CIRCLE[0] + X, INSIDE_CIRCLE[1] + Y,
                                  INSIDE_CIRCLE[2] * 2)
            '''
            cv.namedWindow('', 0)
            cv.resizeWindow('', 1000, 1000)
            cv.imshow('', HAVE_RED_RECT_CIRCLE)
            cv.waitKey()
            '''

        else:
            result_data[label] = (circle_x, circle_y,
                                  0, 0, 0)

    return result_data


def CALCULATE_DATA(data, image):
    """
    绘制标签，根据标签输入小圆真实直径；计算误差并绘制到
    计算：两圆心的真实距离 = (两圆心的像素距离 / 小圆像素直径) * 小圆真实直径
    :param data: INSIDE_DETECT返回的字典数据，key标签:value大圆像素坐标、小圆像素坐标、小圆像素直径
    :param image: 图像
    :return: 计算结果、图像
    """
    # 绘制标签
    cont = len(data)
    for label in range(1, cont + 1):
        CIRCLE_x = data[label][0]  # 大圆x坐标
        CIRCLE_y = data[label][1]  # 大圆y坐标
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, "{}".format(label), (zhuanyong_INT(CIRCLE_x), zhuanyong_INT(CIRCLE_y - 30)),
                   font, 3, (255, 248, 240), 15)
    cv.namedWindow('', 0)
    cv.resizeWindow('', 1600, 800)
    cv.imshow('', image)

    # 输入真实数据与标签
    INPUT_DATA = getInput('请输入', '空格隔开,enter确定,圆的编号=数据')
    INPUT_DATA = INPUT_DATA.split(' ')
    if INPUT_DATA:
        result = {}
        try:
            for DATA in INPUT_DATA:
                label = DATA[0]
                label = int(label)
                CIRCLE_x = data[label][0]  # 大圆x坐标
                CIRCLE_y = data[label][1]  # 大圆y坐标
                circle_x = data[label][2]  # 大圆x坐标
                circle_y = data[label][3]  # 小圆y坐标
                d = data[label][4]  # 小圆像素直径
                Td = float(DATA[2])  # 小圆真实直径

                # 两圆心的真实距离 S = (两圆心的像素距离 / 小圆像素直径) * 小圆真实直径
                S = (calculate_center(CIRCLE_x, CIRCLE_y, circle_x, circle_y) / d) * Td
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(image, "{:0.3f}mm".format(S),
                           (zhuanyong_INT(CIRCLE_x - 80), zhuanyong_INT(CIRCLE_y - 100)),
                           font, 1, (60, 20, 220), 3)
                result[label] = S
        except Exception:
            print('wrong')
    else:
        result = None
        print('未输入数据，跳过运算')

    return result, image, INPUT_DATA


if __name__ == '__main__':
    for x, y, z in os.walk(r'D:\resource_AI\THE DETECTION OF CIRCLE\SAMLPS\testdata'):
        for name in z:
            filepath = r'D:\resource_AI\THE DETECTION OF CIRCLE\SAMLPS\testdata\{}'.format(name)
            src_img = cv.imread(filepath)
            img = cv.imread(filepath)
            print(filepath)
            # cv.circle直接在原图上进行了修改，所以传入的img会发生变化
            OUTSIDE_circle_data = OUTSIDE_detect_circles(img)
            finally_data = INSIDE_DETECT(OUTSIDE_circle_data, img, src_img)
            result, RESULT_IMAGE, INPUTDATA = CALCULATE_DATA(finally_data, img)
            result_path = r'D:\resource_AI\THE DETECTION OF CIRCLE\SAMLPS\result\{}'.format(name)
            cv.imwrite(result_path, RESULT_IMAGE)
            cv.namedWindow('', 0)
            cv.resizeWindow('', 1600, 800)
            cv.imshow('', RESULT_IMAGE)
            cv.waitKey()

            path = r'D:\resource_AI\THE DETECTION OF CIRCLE\测试记录.xls'
            excel_data = xlrd.open_workbook(path)
            sheet = excel_data.sheet_by_index(0)
            row_all = sheet.nrows
            save_excel(row_all, 0, result_path, path)
            save_excel(row_all, 1, INPUTDATA, path)
            save_excel(row_all, 2, '{}'.format(result), path)
            save_excel(row_all, 4, '{}'.format(finally_data), path)
