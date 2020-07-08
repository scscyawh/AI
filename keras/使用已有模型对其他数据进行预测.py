import tensorflow as tf
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

# 读取数据
filepath = 'D://data//numbers//'
file1 = os.listdir(filepath)
filepath = [os.path.join(filepath, x) for x in file1]

# 规范数据与预处理
img = []
for x in filepath:
    data = cv.imread(x)
    data = cv.resize(data, (28, 28))
    data = cv.cvtColor(data, cv.COLOR_BGR2GRAY)
    ret, data = cv.threshold(data, 50, 255, cv.THRESH_BINARY)
    data = cv.dilate(data,
                     kernel=cv.getStructuringElement(cv.MORPH_RECT, (1, 2)),
                     iterations=1)
    # cv.imshow('', data)
    # cv.waitKey()
    img.append(data)
    #print(x)

# 数据一定要保证高度一致，在minst中的数据集也是np.array类型
img = (np.array(img)) / 255.0

# 加载模型
model = tf.keras.models.load_model('D://data//model//minst-numbers.h5')
predictions = model.predict(img)

# 预测结果可视化
# plt.figure(figsize=(8, 8))
for i in range(len(img)):
    plt.subplot(1, 2,  1)
    plt.imshow(img[i])
    plt.subplot(1, 2,  2)
    plt.bar(range(0, 10, 1), predictions[i])
    plt.xticks(range(0, 10, 1))
    plt.yticks(np.linspace(0, 1, 10))
    plt.grid(False)
    plt.xlabel('PX={:2.0f}% pre_label is {}'.format(100 * np.max(predictions[i]), np.argmax(predictions[i])))
    plt.show()
