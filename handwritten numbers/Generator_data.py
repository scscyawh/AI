from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os
import numpy as np


'''
图片生成器，能扩充数据集.
rotation_range—旋转，width_shift_range—水平平移
shear_range-透视，zoom_range—缩放，horziontal-水平反转
'''
datagen = ImageDataGenerator(rotation_range=0.2,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True,
                             fill_mode='nearest')


# 自定义图片生成接口函数
def generator(file):
    filename = os.listdir(file)
    path = [os.path.join(file, x) for x in filename]
    img = []
    for x in path:
        data = load_img(x)
        data = img_to_array(data)
        img.append(data)
    img = np.array(img)
    i = 0

    for batch in datagen.flow(img,
                              batch_size=1,
                              save_to_dir=r'D:\data\MNIST\test\9',
                              save_prefix='9',
                              save_format='png'):
        i = i + 1
        if i > 5000:
            break


generator('D:\\data\\MNIST\\all\\9')
