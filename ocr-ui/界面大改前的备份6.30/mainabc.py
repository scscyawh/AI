from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from PyQt5.QtCore import *
import dlocr
import time
from test import Ui_MainWindow

import socket
import requests
import os
import re
from requests_toolbelt import MultipartEncoder

HOST = '192.168.3.145'
PORT = 8888
BUFSIZE = 1024
share_path = r'\\DESKTOP-MMAR1UQ\test'
search_optimize = 'http://192.168.3.63:8080/upload/optimizeNameplateId?nameplateId='
sign = 'http://192.168.3.63:8080/visionUserLogin?userName='


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    download_dir = ''
    first_click = True

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.pushButton_srcImg.clicked.connect(self.pushButton_srcImg_clicked)
        self.pushButton_ocr.clicked.connect(self.pushButton_ocr_clicked)
        self.pushButton_nameplate_modify.clicked.connect(self.pushButton_nameplate_modify_clicked)
        self.pushButton_download.clicked.connect(self.pushButton_download_clicked)
        self.pushButton_download_start.clicked.connect(self.pushButton_download_start_clicked)
        self.pushButton_upload.clicked.connect(self.pushButton_upload_clicked)
        self.pushButton_close.clicked.connect(self.pushButton_close_clicked)
        self.pushButton_uoloadplate_modify.clicked.connect(self.pushButton_uoloadplate_modify_clicked)
        self.pushButton_upload_start.clicked.connect(self.pushButton_upload_start_clicked)
        self.pushButton_download_find.clicked.connect(self.pushButton_download_find_clicked)
        self.pushButton_exit.clicked.connect(self.pushButton_exit_clicked)
        self.pushButton_sign.clicked.connect(self.pushButton_sign_clicked)

        thread = MyThread()
        thread.start()
        thread.sec_changed_signal.connect(self.update)
        thread.sec_changed_signal2.connect(self.recve)
        self.pushButton_srcImg.clicked.connect(lambda: thread.start())

    def recve(self, s_con):
        return s_con

    def update(self, data):
        self.textEdit_srcImg.setText(data)

        # 显示图片
        if '正在识别----数据接收成功:' in data:
            end = len(data)
            src_img_path = data[15: end]
            self.img_path = src_img_path
            try:
                imageObj = QImage()
                imageObj.load(self.img_path)
                pix = QtGui.QPixmap.fromImage(imageObj)
                self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
                self.scene = QGraphicsScene()  # 创建场景
                self.scene.addItem(self.item)
                self.graphicsView.setScene(self.scene)  # 将场景添加至视图
                self.graphicsView.fitInView(QGraphicsPixmapItem(pix))  # 图像自适应大小
            except Exception:
                self.textEdit_ocr.setText("路径未找到，图片加载失败")
                self.textEdit_nameplate.setText("路径未找到，图片加载失败")

        # 识别结果展示
        if '识别成功:' in data:
            end = len(data)
            result = data[5: end]
            self.textEdit_ocr.setText(result)
            self.textEdit_nameplate.setText(result)

    def pushButton_exit_clicked(self):
        exit()

    def pushButton_sign_clicked(self):
        print("点击按钮登录按钮")
        try:
            print("开始登录")
            username = self.Edit_sign.toPlainText()
            print("username=", username)
            password = self.Edit_password.text()
            print("password=", password)
            url = "{}{}".format(sign, username)
            print("url=", url)
            rs = requests.get(url)
            True_password = rs.text
            print("True_password=", True_password)
            if password == True_password:
                QMessageBox.information(self, '提示', '登录成功', QMessageBox.Yes)
                self.frame_3.setVisible(True)
                self.frame.setVisible(True)
                self.frame_sign.setVisible(False)
                self.Edit_password.setVisible(False)
                self.Edit_sign.setVisible(False)
                self.pushButton_sign.setVisible(False)
                self.pushButton_exit.setVisible(False)
            else:
                QMessageBox.information(self, '提示', '登录失败请重试', QMessageBox.Yes)
        except Exception:
            QMessageBox.information(self, '提示', '连接超时，请重试', QMessageBox.Yes)

    def pushButton_download_find_clicked(self):
        download_file_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                        "选择本地下载路径"
                                                                        )
        self.textEdit_download_pc.setText(download_file_path)

    def pushButton_close_clicked(self):
        exit()

    def pushButton_ocr_clicked(self):
        try:
            print("-----------------start ocr----------------")
            # ------ocr start-----
            start_time = time.time()
            bboxes, texts = ocr.detect(self.img_path)
            result_line = texts
            if result_line is None:
                result_line = "未识别到"
            end_time = time.time()
            print("cost={:0.2f}s".format(end_time - start_time))
            # ------ocr over -----
            self.textEdit_ocr.setText(result_line)
            self.textEdit_nameplate.setText(result_line)
        except Exception:
            QMessageBox.warning(self, '错误！', '识别失败，可能是因为图片太大')
            self.textEdit_ocr.setText("未识别到")
            self.textEdit_nameplate.setText("未识别到")

    def pushButton_uoloadplate_modify_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_upload_url.setReadOnly(False)
            self.pushButton_uoloadplate_modify.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_upload_url.setReadOnly(True)
            self.pushButton_uoloadplate_modify.setText("修改")
            MainWindow.first_click = True

    def pushButton_nameplate_modify_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_nameplate.setReadOnly(False)
            self.pushButton_nameplate_modify.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_nameplate.setReadOnly(True)
            self.pushButton_nameplate_modify.setText("修改")
            MainWindow.first_click = True

    def pushButton_download_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_download.setReadOnly(False)
            self.pushButton_download.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_download.setReadOnly(True)
            self.pushButton_download.setText("修改")
            MainWindow.first_click = True

    def pushButton_download_start_clicked(self):

        try:
            # nameplateId=01-BD01
            # 请求响应的接口
            http_pre = self.textEdit_download.toPlainText()

            # 获取铭牌号
            number = self.textEdit_nameplate.toPlainText()

            # 请求响应的接口以及传递的参数
            request_url = http_pre + number
            print("(请求响应)的接口以及其(需要传递)的参数：", request_url)

            # 开始请求响应  res为响应的结果
            print("--------开始请求----------")
            res = requests.get(request_url)
            # 将响应的结果自动按默认utf-8解码
            download_url = res.text
            print("得到响应的结果后进行解码操作：" + download_url)

            filename = os.path.basename(download_url)
            print("filename:" + filename)
            path_str = self.textEdit_download_pc.toPlainText() + "/" + filename
            print("path_str:" + path_str)

            with open(path_str, "wb") as f:
                f.write(requests.get(download_url).content)
            QMessageBox.information(self, "提示", "下载完成", QMessageBox.Yes)
        except Exception:
            QMessageBox.warning(self, '错误！', '下载失败')

    def pushButton_upload_clicked(self):
        upload_file_path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                 "选择上传文件",
                                                                 MainWindow.download_dir,
                                                                 "All Files(*.xls *.xlsx)"
                                                                 )
        self.textEdit_upload.setText(upload_file_path[0])

    def pushButton_upload_start_clicked(self):
        try:
            #
            print("pushButton")
            # 请求的接口url
            url = self.textEdit_upload_url.toPlainText()
            print("上传的网址：", url)
            nameplateId = self.textEdit_nameplate.toPlainText()
            print("检具名：", nameplateId)
            file_path = self.textEdit_upload.toPlainText()

            print("file_path:" + file_path)
            file_name = os.path.basename(file_path)

            data = MultipartEncoder(
                fields={
                    'nameplateId': (None, nameplateId),
                    # 'field_0':(None, 'value_n'),
                    'file': (file_name, open(file_path, 'rb'), 'text/plain'),
                }
            )

            r = requests.post(url, data, headers={'Content-Type': data.content_type})
            QMessageBox.information(self, "提示", "上传完成", QMessageBox.Yes)

        except Exception:
            QMessageBox.warning(self, '错误！', '上传失败')


class MyThread(QThread):
    sec_changed_signal = pyqtSignal(str)
    sec_changed_signal2 = pyqtSignal(socket.socket)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            s_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            s_server.bind((HOST, PORT))
            while 1:
                s_server.listen(5)
                self.sec_changed_signal.emit("等待连接")
                s_con, addr = s_server.accept()
                self.sec_changed_signal2.emit(s_con)
                self.sec_changed_signal.emit('从{}连接成功,等待接收数据'.format(addr))
                while 1:
                    try:
                        filename = s_con.recv(BUFSIZE)
                        if not filename:
                            break
                    except Exception:
                        break
                    print("-------------------------------------------------------")
                    s_con.send(str.encode('[%s]%s' % (time.ctime(), filename)))
                    filename = str(filename, encoding='utf-8')
                    src_img_path = r"{}\{}".format(share_path, filename)
                    print(src_img_path)
                    self.sec_changed_signal.emit("正在识别----数据接收成功:{}".format(src_img_path))
                    x, y = ocr.detect(src_img_path)
                    print("优化前:", y)
                    try:
                        print('url={}{}'.format(search_optimize, y))
                        re1 = requests.get('{}{}'.format(search_optimize, y))
                        y_optim = re1.text
                        print("优化后:", y_optim)
                        if len(y_optim) > 100:
                            y_optim = y
                    except Exception:
                        print('模糊查询失败')
                    if y_optim is None:
                        y_optim = '未识别到'
                    self.sec_changed_signal.emit('识别成功:{}'.format(y_optim))
                    s_con.send(str.encode(y_optim))
        except Exception:
            s_con.close()
            s_server.close()
            self.sec_changed_signal.emit('未找到图片，服务器已关闭，请重启服务器')


import sys

if __name__ == "__main__":
    ocr = dlocr.get_or_create()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
