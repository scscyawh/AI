import cv2 as cv
import os
import numpy as np


def detect_straight(PATH):
    img = cv.imread(PATH)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, img_threshold = cv.threshold(img_gray, 50, 255, cv.THRESH_BINARY)

    lines = cv.HoughLinesP(img_threshold, 1, np.pi / 180, 30, maxLineGap=10)
    if lines is not None:
        print('----------------------------{}----------------------------'.format(len(lines)))
        print(lines)
        for line in lines:
            x1 = line[0][0]
            y1 = line[0][1]
            x2 = line[0][2]
            y2 = line[0][3]

            # 先合并

            cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(img, 'S|y1:{}'.format(y1), (x1, y1+50), font, 1, (255, 255, 255), 1)
            cv.putText(img, 'E|y2:{}'.format(y2), (x2, y2-50), font, 1, (0, 255, 0), 1)

        cv.namedWindow('', 0)
        cv.resizeWindow('', 1600, 1000)
        cv.imshow('', img)
        cv.waitKey()
    else:
        print('nothing')


if __name__ == '__main__':
    for x, y, z in os.walk(r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA'):
        for filename in z:
            path = r'D:\resource_AI\THE DETECTION OF STRA\TESTDATA\{}'.format(filename)
            detect_straight(path)
