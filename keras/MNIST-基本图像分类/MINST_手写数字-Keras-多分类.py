import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2 as cv

# 下载数据，保存在C:\Users\Hasee\.keras。存在则直接读取
mnist = tf.keras.datasets.mnist
# 加载数据，此语句返回的4个变量(x_train(i) ，etc)是numpy中的N维数组(np.array)
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 此数据为图像，将图像的每一个像素点除255，类似与将他们百分化。
x_train, x_test = x_train/255.0, x_test/255.0
for x in range(len(x_train)):
    print(x_train[x].shape)

# 显示前100个训练集中的图像
plt.figure(figsize=(25, 10))
for i in range(100):
    plt.subplot(10, 10, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_train[i])
    plt.xlabel(y_train[i])
plt.show()

# 判断模型是否存在，不存在则建立-编译-训练模型
if os.path.exists("D://data//model//minst-numbers.h5") is True:
    print("模型已加载")
    model = tf.keras.models.load_model("D://data//model//minst-numbers.h5")
else:
    print("正在建立-训练模型")
    # 建立模型-设置图层(神经网络基本构建块是图层)
    # Sequential是一个序贯模型
    model = tf.keras.models.Sequential([
        # Flatten将图像的格式从2d矩阵(28像素X28像素)转成784像素的1d阵列.
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        # Dense由两层序列组合，第一层有784神经元。
        tf.keras.layers.Dense(784, activation='relu'),
        # Dropout是剪枝操作，使得部分训练参数失效，避免过度拟合。
        # 过度拟合是指机器学习模型在新数据上的表现比在训练数据上更差。
        tf.keras.layers.Dropout(0.2),
        # 这是Dense的第二层，由10个神经元组成的的softmax层，
        # softmax层将返回10个概率分数的数组，10个概率总和为1。每个节点表示当前图像属于10个类之一的概率分数
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # 编译模型；模型准备好后，在训练之前还要进行更多的设置。
    # optimizer——优化器-这是基于它看到的数据及其损失函数更新模型的方式。
    # loss     ——损失/代价函数 - 这可以衡量模型在训练过程中的准确程度，
    # 我们希望最小化此功能，以便在正确的方向上“引导”模型。
    # metric   ——度量标准 - 用于监控培训和测试步骤。以下示例使用精度，即正确分类的图像的分数。
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # 训练模型，迭代5次
    model.fit(x_train, y_train, epochs=20)
    print("训练结束")
    # 保存模型
    model.save("D://data//model//minst-numbers.h5")


# 用测试集评估模型
test_loss, test_acc = model.evaluate(x_test, y_test)
print('损失度：', test_loss)
print('精确度：', test_acc)

# 预测(使用模型)
print('------------------预测------------------')
# 此函数返回的predictions[i]是numpy中的N维数组,np.array
predictions = model.predict(x_test)

print('测试集中第一个图像的10个标签的概率分布', predictions[0])
print('取出其中概率最大的值对应的索引(数组下标)', np.argmax(predictions[0]))
print('标签为：', y_test[0])
print('概率100分比是', 100*np.max(predictions[0]))


# 预测(可视化版)
def plot_image(i):
    plt.imshow(x_test[i])
    plt.xticks([])
    plt.yticks([])
    plt.xlabel("p= {:2.2f}% (label is {})".format(100 * np.max(predictions[i]), y_test[i]))
    plt.grid(False)

def plot_px(i) :
    plt.bar(range(10), predictions[i])
    plt.xticks(range(0, 10, 1))
    plt.grid(False)


for x in range(25):
    plt.subplot(5, 10, 2*x+1)
    plot_image(x)
    plt.subplot(5, 10, 2*x+2)
    plot_px(x)
plt.show()

px = 0
for al in range(len(x_test)):
    if np.argmax(predictions[al]) == y_test[al] :
        continue
    else:
        px = px + 1
print('判断错误'+str(px)+"次")
print('错误概率为'+str(100*(px/10000))+'%')
