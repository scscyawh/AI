import tensorflow as tf
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img, img_to_array

model = tf.keras.models.load_model('hand_writting.h5')

##################
# 手绘
filename = os.listdir('test/')
filename = [os.path.join('test/', x) for x in filename]
data = []
for x in filename:
    img = cv.imread(x)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    data.append(img)
data = np.array(data)
data1 = np.array(data)
data = data / 255.0
data = np.expand_dims(data, axis=3)

pre = model.predict(data)

plt.figure(figsize=(8, 8))
print(pre[0])
for x in range(20):
    plt.subplot(4, 10, 2 * x + 1)
    plt.imshow(data1[x])
    plt.xlabel('max_p={:0.2f} pre_label={}'.format(np.max(pre[x]), np.argmax(pre[x])))
    plt.subplot(4, 10, 2 * x + 2)
    plt.bar(range(10), pre[x])
    plt.xticks(range(10))
    plt.yticks(np.linspace(0, 1, 10))
    plt.grid(True)
plt.show()


#######################
# 测试集
test = []
label = []
for x in range(10):
    f = os.listdir('Train_Validation/test/{}'.format(x))
    f = [os.path.join('Train_Validation/test/{}//'.format(x), w) for w in f]
    for name in f:
        img = load_img(name)
        img = img_to_array(img)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        test.append(img)
        label.append(x)
test = np.array(test)
test = test/255.0
test = np.expand_dims(test, axis=3)
label = np.array(label)
label2 = np.array(label)
label = tf.keras.utils.to_categorical(label, num_classes=10)
print(label)

pre2 = model.predict(test)

flag = 0
for i in range(len(pre2)):
    if np.argmax(pre2[i]) == label2[i]:
        continue
    else:
        flag = flag + 1
        print('Wrong! pre_label is {}, T_label is {}'.format(np.argmax(pre2[i]), label2[i]))
print('-----------------------------------')
print('总共{}张图片，预测错误{}张，错误率为{:0.2f}%'.format(len(pre2), flag, 100*(flag/(len(pre2)))))
