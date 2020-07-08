import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt

MNIST_fasion = tf.keras.datasets.fashion_mnist
(data_train, data_label), (test_train, teat_label) = MNIST_fasion.load_data()
data_train, test_train = data_train / 255.0, test_train / 255.0

# 类名并不在label中，所以我们人工添加，方便可视化等
class_name = ['T-shirt', 'Trouser', 'Pullover',
              'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker',
              'Bag', 'Ankle boot ']

plt.figure(figsize=(8, 8))
for i in range(50):
    plt.subplot(5, 10, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.ylabel([])
    plt.grid(False)
    plt.imshow(data_train[i])
    plt.colorbar()
    plt.xlabel(class_name[data_label[i]])
plt.show()

if os.path.exists("D:\\data\\model\\minst-fashion.h5") is True:
    print("加载模型")
    model = tf.keras.models.load_model("D:\\data\\model\\minst-fashion.h5")
else:
    print("模型不存在，创建-编译-训练模型")
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
    model.add(tf.keras.layers.Dense(784, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(data_train, data_label, epochs=20)
    print("训练结束")
    model.save("D:\\data\\model\\minst-fashion.h5")

    # 绘制训练过程中的acc、loss 与 epochs之间的关系
    history_dict = history.history
    acc = history_dict['acc']
    loss = history_dict['loss']
    epochs = range(1, 21)
    plt.figure(figsize=(8, 8))
    plt.plot(epochs, acc, 'b', label='acc')
    plt.plot(epochs, loss, 'r', label='loss')
    plt.xlabel('epochs')
    plt.ylabel('data')
    plt.legend()
    plt.show()

loss, acc = model.evaluate(test_train, teat_label)
print("loss:", loss)
print("acc:", acc)

predictions = model.predict(test_train)


def plot_img(x):
    if np.argmax(predictions[x]) == teat_label[x]:
        color = 'blue'
    else:
        color = 'red'
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(test_train[x], cmap=plt.cm.binary)
    plt.xlabel("pre={} {:2.0f}% True=({})".format(class_name[np.argmax(predictions[x])],
                                                  100 * np.max(predictions[x]),
                                                  class_name[teat_label[x]]),
               color=color)


for u in range(15):
    plt.subplot(3, 5, u + 1)
    plot_img(u)
plt.show()

px = 0

for al in range(len(test_train)):
    if np.argmax(predictions[al]) == teat_label[al]:
        continue
    else:
        px = px + 1

print('判断错误' + str(px) + "次")
print('错误概率为' + str(100 * (px / 10000)) + '%')
