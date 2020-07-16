from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage, QCursor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from PyQt5.QtCore import *
import dlocr
import time
from my_frame import Ui_MainWindow

import cv2 as cv
from dlocr import CHoughCircles
import socket
import requests
import os
import re
from requests_toolbelt import MultipartEncoder

HOST = '192.168.3.145'  # "192.168.0.102"
PORT = 8888
BUFSIZE = 1024
share_path = r'C:\Users\Hasee\Desktop\test'
search_optimize = 'http://192.168.3.174:8080/upload/optimizeNameplateId?nameplateId='
sign = 'http://192.168.3.174:8080/visionUserLogin?userName='


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    download_dir = ''
    first_click = True
    HOST_PUSHDOWN_first_click = True
    SUPPLY_PUSHDOWN_first_click = True

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_nameplate_modify.clicked.connect(self.pushButton_nameplate_modify_clicked)
        self.pushButton_download.clicked.connect(self.pushButton_download_clicked)
        self.pushButton_download_start.clicked.connect(self.pushButton_download_start_clicked)
        self.pushButton_host_upfile.clicked.connect(self.pushButton_host_upfile_clicked)
        self.pushButton_close.clicked.connect(self.pushButton_close_clicked)
        self.pushButton_host_upstart.clicked.connect(self.pushButton_upload_start_clicked)
        self.pushButton_download_find.clicked.connect(self.pushButton_download_find_clicked)
        self.pushButton_exit.clicked.connect(self.pushButton_exit_clicked)
        self.pushButton_sign.clicked.connect(self.pushButton_sign_clicked)
        self.pushButton_Min.clicked.connect(self.pushButton_Min_clicked)
        self.change_analysis.clicked.connect(self.change_analysis_clicked)
        self.change_host.clicked.connect(self.change_host_clicked)
        self.change_supply.clicked.connect(self.change_supply_clicked)
        self.pushButton_host_upload_modify.clicked.connect(self.pushButton_host_upload_modify_clicked)
        self.pushButton_nameplate_modify_su.clicked.connect(self.pushButton_nameplate_modify_su_clicked)
        self.pushButton_download_su.clicked.connect(self.pushButton_download_su_clicked)
        self.pushButton_download_find_su.clicked.connect(self.pushButton_download_find_su_clicked)
        self.pushButton_download_start_su.clicked.connect(self.pushButton_download_start_su_clicked)
        self.pushButton_supply_upload_modify.clicked.connect(self.pushButton_supply_upload_modify_clicked)
        self.pushButton_supply_upfile.clicked.connect(self.pushButton_supply_upfile_clicked)
        self.pushButton_supply_upstart.clicked.connect(self.pushButton_supply_upstart_clicked)
        self.HOST_PUSHDOWN.clicked.connect(self.HOST_PUSHDOWN_clicked)
        self.SUPPLY_PUSHDOWN.clicked.connect(self.SUPPLY_PUSHDOWN_clicked)

        thread = MyThread()
        thread.start()
        thread.sec_changed_signal.connect(self.update)
        thread.sec_changed_signal2.connect(self.recve)
        self.pushButton_srcImg.clicked.connect(lambda: (thread.start(),
                                                        QMessageBox.information(self, '提示', '成功'),))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def change_analysis_clicked(self):
        self.groupBox.setVisible(True)
        self.groupBox_3.setVisible(False)
        self.groupBox_4.setVisible(False)

    def change_host_clicked(self):
        self.groupBox.setVisible(False)
        self.groupBox_3.setVisible(True)
        self.groupBox_4.setVisible(False)

    def change_supply_clicked(self):
        self.groupBox.setVisible(False)
        self.groupBox_3.setVisible(False)
        self.groupBox_4.setVisible(True)

    def pushButton_Min_clicked(self):
        self.showMinimized()

    def recve(self, time):
        self.textEdit_cost.setText(time)

    def update(self, data):
        self.textEdit_srcImg.setText(data)
        # 显示图片
        if '正在识别----数据接收成功----' in data:
            end = len(data)
            src_img_path = data[18: end]
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
        if '识别结束                ' in data:
            end = len(data)
            result = data[20: end]
            self.textEdit_nameplate_su.setText(result)
            self.textEdit_nameplate.setText(result)
            self.textEdit_ocr.setText(result)
            self.textEdit_srcImg.setText("识别结束")

    def pushButton_exit_clicked(self):
        exit()

    def pushButton_sign_clicked(self):
        '''
        try:
            print("----------------开始登录-------------------")
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
            '''
        QMessageBox.information(self, '提示', '登录成功', QMessageBox.Yes)
        self.frame_3.setVisible(True)
        self.frame.setVisible(True)
        self.frame_background.setVisible(True)
        self.frame_sign.setVisible(False)
        self.Edit_password.setVisible(False)
        self.Edit_sign.setVisible(False)
        self.pushButton_sign.setVisible(False)
        self.pushButton_exit.setVisible(False)
        '''
            else:
                QMessageBox.information(self, '提示', '登录失败请重试', QMessageBox.Yes)
        except Exception:
            QMessageBox.information(self, '提示', '连接超时，请重试', QMessageBox.Yes)
        '''

    def pushButton_download_find_su_clicked(self):
        download_file_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                        "选择本地下载路径"
                                                                        )
        self.textEdit_download_pc_su.setText(download_file_path)

    def pushButton_download_find_clicked(self):
        download_file_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                        "选择本地下载路径"
                                                                        )
        self.textEdit_download_pc.setText(download_file_path)

    def pushButton_close_clicked(self):
        exit()

    def SUPPLY_PUSHDOWN_clicked(self):
        if MainWindow.SUPPLY_PUSHDOWN_first_click == True:
            self.label_3_su.setVisible(False)
            self.textEdit_download_su.setVisible(False)
            self.label_7_su.setVisible(False)
            self.textEdit_download_pc_su.setVisible(False)
            self.pushButton_download_find_su.setVisible(False)
            self.pushButton_download_start_su.setVisible(False)
            self.pushButton_download_su.setVisible(False)

            self.label_supply_upload.setVisible(True)
            self.textEdit_supply_upload.setVisible(True)
            self.pushButton_supply_upload_modify.setVisible(True)
            self.label_supply_upfile.setVisible(True)
            self.textEdit_supply_upfile.setVisible(True)
            self.pushButton_supply_upfile.setVisible(True)
            self.pushButton_supply_upstart.setVisible(True)
            MainWindow.SUPPLY_PUSHDOWN_first_click = False
        else:
            self.label_3_su.setVisible(True)
            self.textEdit_download_su.setVisible(True)
            self.label_7_su.setVisible(True)
            self.textEdit_download_pc_su.setVisible(True)
            self.pushButton_download_find_su.setVisible(True)
            self.pushButton_download_start_su.setVisible(True)
            self.pushButton_download_su.setVisible(True)

            self.label_supply_upload.setVisible(False)
            self.textEdit_supply_upload.setVisible(False)
            self.pushButton_supply_upload_modify.setVisible(False)
            self.label_supply_upfile.setVisible(False)
            self.textEdit_supply_upfile.setVisible(False)
            self.pushButton_supply_upfile.setVisible(False)
            self.pushButton_supply_upstart.setVisible(False)
            MainWindow.SUPPLY_PUSHDOWN_first_click = True

    def HOST_PUSHDOWN_clicked(self):
        if MainWindow.HOST_PUSHDOWN_first_click == True:
            self.label_3.setVisible(False)
            self.textEdit_download.setVisible(False)
            self.pushButton_download.setVisible(False)
            self.label_7.setVisible(False)
            self.textEdit_download_pc.setVisible(False)
            self.pushButton_download_find.setVisible(False)
            self.pushButton_download_start.setVisible(False)

            self.label_host_upload.setVisible(True)
            self.textEdit_host_upload.setVisible(True)
            self.pushButton_host_upload_modify.setVisible(True)
            self.label_host_upfile.setVisible(True)
            self.textEdit_host_upfile.setVisible(True)
            self.pushButton_host_upfile.setVisible(True)
            self.pushButton_host_upstart.setVisible(True)
            MainWindow.HOST_PUSHDOWN_first_click = False
        else:
            self.label_3.setVisible(True)
            self.textEdit_download.setVisible(True)
            self.pushButton_download.setVisible(True)
            self.label_7.setVisible(True)
            self.textEdit_download_pc.setVisible(True)
            self.pushButton_download_find.setVisible(True)
            self.pushButton_download_start.setVisible(True)

            self.label_host_upload.setVisible(False)
            self.textEdit_host_upload.setVisible(False)
            self.pushButton_host_upload_modify.setVisible(False)
            self.label_host_upfile.setVisible(False)
            self.textEdit_host_upfile.setVisible(False)
            self.pushButton_host_upfile.setVisible(False)
            self.pushButton_host_upstart.setVisible(False)
            MainWindow.HOST_PUSHDOWN_first_click = True

    def pushButton_supply_upload_modify_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_supply_upload.setReadOnly(False)
            self.pushButton_supply_upload_modify.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_supply_upload.setReadOnly(True)
            self.pushButton_supply_upload_modify.setText("修改")
            MainWindow.first_click = True

    def pushButton_download_su_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_download_su.setReadOnly(False)
            self.pushButton_download_su.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_download_su.setReadOnly(True)
            self.pushButton_download_su.setText("修改")
            MainWindow.first_click = True

    def pushButton_nameplate_modify_su_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_nameplate_su.setReadOnly(False)
            self.pushButton_nameplate_modify_su.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_nameplate_su.setReadOnly(True)
            self.pushButton_nameplate_modify_su.setText("修改")
            MainWindow.first_click = True

    def pushButton_uoloadplate_modify_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_upload_url.setReadOnly(False)
            self.pushButton_uoloadplate_modify.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_upload_url.setReadOnly(True)
            self.pushButton_uoloadplate_modify.setText("修改")
            MainWindow.first_click = True

    def pushButton_host_upload_modify_clicked(self):
        if MainWindow.first_click == True:
            self.textEdit_host_upload.setReadOnly(False)
            self.pushButton_host_upload_modify.setText("完成")
            MainWindow.first_click = False
        else:
            self.textEdit_host_upload.setReadOnly(True)
            self.pushButton_host_upload_modify.setText("修改")
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

    def pushButton_download_start_su_clicked(self):
        try:
            print('----------------开始下载-------------------')
            # nameplateId=01-BD01
            # 请求响应的接口
            http_pre = self.textEdit_download_su.toPlainText()

            # 获取铭牌号
            number = self.textEdit_nameplate_su.toPlainText()

            # 请求响应的接口以及传递的参数
            request_url = http_pre + number
            print("(请求响应)的接口以及其(需要传递)的参数：", request_url)

            # 开始请求响应  res为响应的结果
            res = requests.get(request_url)
            # 将响应的结果自动按默认utf-8解码
            download_url = res.text
            print("得到响应的结果后进行解码操作：" + download_url)

            filename = os.path.basename(download_url)
            print("filename:" + filename)
            path_str = self.textEdit_download_pc_su.toPlainText() + "/" + filename
            print("path_str:" + path_str)

            with open(path_str, "wb") as f:
                f.write(requests.get(download_url).content)
            QMessageBox.information(self, "提示", "下载完成", QMessageBox.Yes)
        except Exception:
            QMessageBox.warning(self, '错误！', '下载失败')

    def pushButton_download_start_clicked(self):
        try:
            print('----------------开始下载-------------------')
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

    def pushButton_supply_upfile_clicked(self):
        upload_file_path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                 "选择上传文件",
                                                                 MainWindow.download_dir,
                                                                 "All Files(*.xls *.xlsx)"
                                                                 )
        self.textEdit_supply_upfile.setText(upload_file_path[0])

    def pushButton_host_upfile_clicked(self):
        upload_file_path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                 "选择上传文件",
                                                                 MainWindow.download_dir,
                                                                 "All Files(*.xls *.xlsx)"
                                                                 )
        self.textEdit_host_upfile.setText(upload_file_path[0])

    def pushButton_supply_upstart_clicked(self):
        try:
            #
            print('----------------开始上传-------------------')
            # 请求的接口url
            url = self.textEdit_supply_upload.toPlainText()
            print("上传的网址：", url)
            nameplateId = self.textEdit_nameplate_su.toPlainText()
            print("检具名：", nameplateId)
            file_path = self.textEdit_supply_upfile.toPlainText()

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

    def pushButton_upload_start_clicked(self):
        try:
            #
            print('----------------开始上传-------------------')
            # 请求的接口url
            url = self.textEdit_host_upload.toPlainText()
            print("上传的网址：", url)
            nameplateId = self.textEdit_nameplate.toPlainText()
            print("检具名：", nameplateId)
            file_path = self.textEdit_host_upfile.toPlainText()

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
    sec_changed_signal2 = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        global y_optim, filename
        try:
            flag = 0
            s_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            s_server.bind((HOST, PORT))
            while 1:
                s_server.listen(5)
                self.sec_changed_signal.emit("等待连接")
                s_con, addr = s_server.accept()
                self.sec_changed_signal.emit('从{}连接成功,等待接收数据'.format(addr))
                while 1:
                    try:
                        re_data = s_con.recv(BUFSIZE)
                        if not re_data:
                            break
                    except Exception:
                        break
                    print("-------------------{}-----------------------".format(time.ctime()))

                    re_data = str(re_data, encoding='utf-8')
                    print(re_data)
                    re_data = re_data.split(' ')
                    if len(re_data) == 3:
                        filename = re_data[2]
                    else:
                        filename = re_data[1]
                    src_img_path = r"{}\{}".format(share_path, filename)

                    start_run = time.time()
                    if 'LABEL' in re_data[0]:
                        self.sec_changed_signal.emit("正在识别----数据接收成功----{}".format(src_img_path))
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
                            flag = 1
                            self.sec_changed_signal.emit("连接后台服务器失败,请调整后重启服务器!")
                        if y_optim is None:
                            y_optim = 'The detection failed'
                        self.sec_changed_signal.emit('识别结束                {}'.format(y_optim))
                        y_optim = str(y_optim)
                        s_con.send(str.encode('LABEL'+' '+y_optim))
                        end_time = time.time() - start_run
                        self.sec_changed_signal2.emit('{:0.2f}ms'.format(end_time*1000))

                    if 'CIRC' in re_data[0]:
                        INPUT = float(re_data[1])
                        result, image = CHoughCircles.fit_circle(src_img_path, INPUT)
                        cv.imwrite('circles.png', image)
                        result = str(result)
                        s_con.send(str.encode("CIRC"+","+result))
                        self.sec_changed_signal.emit("正在识别----数据接收成功----{}".format('circles.png'))
                        self.sec_changed_signal.emit('识别结束                {}'.format(result))
                        end_time = time.time() - start_run
                        self.sec_changed_signal2.emit('{:0.2f}ms'.format(end_time*1000))

                    if 'MINST' in re_data[0]:
                        pass

        except Exception:
            try:
                s_con.close()
                s_server.close()
                if flag == 0:
                    self.sec_changed_signal.emit('未找到图片，服务器已关闭，请重启服务器')
                flag = 0
            except Exception:
                self.sec_changed_signal.emit('无法启动服务器，请检查IP是否正确')


import sys

if __name__ == "__main__":
    ocr = dlocr.get_or_create()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
