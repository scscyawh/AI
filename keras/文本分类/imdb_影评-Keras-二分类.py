import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt

'''
机器学习处理文本中，会根据语料建立一个字库，用词语所在的数字代替。
这里导入的数据已经全部转换成了数字。

标签的数据只有0和1，分别代表负面评论和证明评论。
'''
imdb = tf.keras.datasets.imdb
(train_data, train_label), (test_data, test_label) = imdb.load_data(num_words=10000)

# 将数字转换成词组
word_index = imdb.get_word_index()
word_index = {k: v + 3 for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3
reverse_word_index = dict([(v, k) for (k, v) in word_index.items()])


def looking(text):
    flag = 0
    for i in text:
        print(reverse_word_index[i], end=' ')
        flag = flag + 1
        if flag % 13 == 0:
            print('\n')


# 用'0'填充数据，在末尾填充，填充至256
train_data = tf.keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"],
                                                           padding='post',
                                                           maxlen=256)
test_data = tf.keras.preprocessing.sequence.pad_sequences(test_data,
                                                          value=word_index["<PAD>"],
                                                          padding='post',
                                                          maxlen=256)

# looking(train_data[0])
# print(train_data[0])

# 构建模型
if os.path.exists("D:\\data\\model\\imdb-keras.h5") is True:
    print('加载模型中')
    model = tf.keras.models.load_model("D:\\data\\model\\imdb-keras.h5")
else:
    print("构建模型-编译模型-训练模型中")
    model = tf.keras.models.Sequential()
    # Embedding将整数转换成向量
    model.add(tf.keras.layers.Embedding(10000, 16))
    # GlobalAveragePooling 全局平均池化
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    histroy = model.fit(train_data, train_label, epochs=40, batch_size=512)
    model.save("D:\\data\\model\\imdb-keras.h5")

    # 绘制训练过程的精度、损失、迭代次数之间的关系
    histroy_dict = histroy.history
    acc = histroy_dict['acc']
    loss = histroy_dict['loss']
    epochs = range(1, 41)
    plt.figure(figsize=(8, 8))
    plt.plot(epochs, loss, 'r', label='loss')
    plt.plot(epochs, acc, 'b', label='acc')
    plt.xlabel('epochs')
    plt.ylabel('data')
    plt.legend()
    plt.show()

result = model.evaluate(test_data, test_label)
print(result)
print('------------------')

# 预测数据
predicitions = model.predict(train_data)

false = 0
for x in range(len(train_data)):
    if predicitions[x] > 0.5:
        predicitions[x] = 1
    else:
        predicitions[x] = 0

    if predicitions[x] != train_label[x]:
        print('pre_label is ' + str(predicitions[x]) +
              '  ' + 'True_label is ' + str(train_label[x]))
        false = false + 1
    else:
        continue

print('------------------')
print('已完成' + str(len(train_data)) + '次' + '错误率为' + str(100 * (false / (len(train_data)))) + '%')
