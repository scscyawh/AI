from keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np
import time
import cv2 as cv
import tensorflow as tf
import matplotlib.pyplot as plt

start = time.time()

print('preprecessing data------')
# 训练集数据读取与预处理
train = []
table = []
for i in range(10):
    filename = os.listdir('Train_Validation/all/{}'.format(i))
    filename = [os.path.join('Train_Validation/all/{}/'.format(i), x) for x in filename]
    for name in filename:
        img = load_img(name)
        img = img_to_array(img)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        train.append(img)
        table.append(i)
train = np.array(train)
train = train / 255.0
train = np.expand_dims(train, axis=3)
print(train.shape)
table = np.array(table)
table = tf.keras.utils.to_categorical(table, num_classes=10)

# 测试集数据读取与预处理
test = []
test_table = []
for i in range(10):
    filename = os.listdir('Train_Validation/test/{}'.format(i))
    filename = [os.path.join('Train_Validation/test/{}/'.format(i), x) for x in filename]
    for name in filename:
        img = load_img(name)
        img = img_to_array(img)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        test.append(img)
        test_table.append(i)
test = np.array(test)
test = test / 255.0
test = np.expand_dims(test, axis=3)
print(test.shape)
test_table = np.array(test_table)
test_table = tf.keras.utils.to_categorical(test_table, num_classes=10)

if os.path.exists('hand_writting.h5'):
    print('loading-------')
    model = tf.keras.models.load_model('hand_writting.h5')
else:
    print('training------')
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
    model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Flatten(input_shape=(28, 28, 1)))

    model.add(tf.keras.layers.Dense(786, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    history = model.fit(train, table, epochs=10)
    model.save('hand_writting.h5')

    # 训练过程的变化
    history_dict = history.history
    acc = history_dict['acc']
    loss = history_dict['loss']
    epochs = range(1, 11)
    plt.figure(figsize=(8, 8))
    plt.xlabel('epochs')
    plt.ylabel('')
    plt.plot(epochs, acc, 'b', label='acc')
    plt.plot(epochs, loss, 'ro', label='loss')
    plt.legend()
    plt.show()

result = model.evaluate(test, test_table)
print('验证集精确率为：{:0.2f}%'.format(result[1] * 100))

print('cost:{:.2f}s'.format((time.time() - start)))
