import imageio
import os


def create_gif(image_list, gif_name, duration=0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


if __name__ == '__main__':
    while 1:
        print("-----------------------------------------")
        print("使用说明：将需要制作成gif的图片放入同一个文件下")
        a = input('请输入存放图片文件夹路径(比如D:\\pic\\):')
        try:
            for x, y, z in os.walk(a):
                result = []
                for filename in z:
                    path = '{}{}'.format(a, filename)
                    result.append(path)
            image_list = result
        except Exception:
            print('未找到路径')
            continue
        b = input('请输入每张图片显示的时间(单位：秒)(比如输入 0.5 ，表示一张图片显示0.5秒):')
        gif_name = '{}标题要长！！！这是您的动图！！！！！！.gif'.format(a)
        duration = b
        try:
            create_gif(image_list, gif_name, duration)
        except Exception:
            print("未找到图片，请重试！")
            continue
        print('已完成--------保存路径为:{}'.format(gif_name))
        os.system("start explorer {}".format(a))
