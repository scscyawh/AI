import time

import keras.backend as K

from dlocr.ctpn import default_ctpn_weight_path, default_ctpn_config_path, get_or_create
from dlocr.ctpn import get_session
import os

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", help="图像位置", default=r'c:/users/hasee/Desktop/24124.png')
    parser.add_argument("--config_file_path", help="模型配置文件位置",
                        default=default_ctpn_config_path)
    parser.add_argument("--weights_file_path", help="模型权重文件位置",
                        default=default_ctpn_weight_path)
    parser.add_argument("--output_file_path", help="标记文件保存位置",
                        default="output")

    args = parser.parse_args()

    K.set_session(get_session())

    image_path = args.image_path  # 图像位置
    config_path = args.config_file_path  # 模型配置路径
    weight_path = args.weights_file_path  # 模型权重位置
    output_file_path = args.output_file_path  # 保存标记文件位置
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)
    ctpn = get_or_create(config_path, weight_path)

    if weight_path is not None:
        ctpn = get_or_create(config_path, weight_path)
    else:
        ctpn = get_or_create(config_path)

    start_time = time.time()
    output_file_path = os.path.join(output_file_path, image_path.split('/')[-1])
    print(output_file_path)
    ctpn.predict(image_path, output_path=output_file_path)
    print("cost ", (time.time() - start_time) * 1000, " ms")
