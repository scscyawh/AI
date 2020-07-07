from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QBrush, QPixmap


HOST_URL_DOWN = 'http://192.168.3.63:8080/upload/selectFastUploadUrl?nameplateId='
HOST_URL_UPLOAD = 'http://192.168.3.63:8080/upload/fastFinsihUploadFile'
SUPPLIER_URL_DOWN = 'http://192.168.3.63:8088/SupplierUpload/selectFastUploadUrl?nameplateId='
SUPPLIER_URL_UPLOAD = 'http://192.168.3.63:8088/SupplierUpload/fastFinsihUploadFile'


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 892)
        MainWindow.setFixedSize(1200, 892)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        # self.verticalLayout.setObjectName("verticalLayout")
        # self.centralwidget.setStyleSheet("background:white")

        '''
        登陆界面
        利用一个新的frame挡住主界面所有东西
        账户密码正确后，再移除这个frame
        '''
        self.frame_sign = QtWidgets.QFrame(self.centralwidget)
        self.frame_sign.setGeometry(QtCore.QRect(20, 20, 1160, 832))
        self.frame_sign.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sign.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sign.setObjectName("frame_sign")
        self.frame_sign.setStyleSheet('''
                                         border-image:url(Helper-tool.jpg);  
                                      ''')

        self.groupBox_sign = QtWidgets.QGroupBox(self.frame_sign)
        self.groupBox_sign.setGeometry(QtCore.QRect(325, 300, 511, 269))
        self.groupBox_sign.setObjectName("groupBox_sign")
        self.groupBox_sign.setStyleSheet('''
                                          border-image:url(872135.png);
                                          font-size:20px;
                                          font-weight:700;
                                          font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                         ''')

        self.Edit_sign = QtWidgets.QTextEdit(self.centralwidget)
        self.Edit_sign.setGeometry(QtCore.QRect(430, 350, 350, 50))
        self.Edit_sign.setObjectName("Edit_sign")
        self.Edit_sign.setStyleSheet('background:white')
        self.Edit_sign.setPlaceholderText("username")

        self.Edit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.Edit_password.setGeometry(QtCore.QRect(430, 430, 350, 50))
        self.Edit_password.setObjectName("Edit_password")
        self.Edit_password.setStyleSheet('background:white')
        self.Edit_password.setPlaceholderText("password")
        self.Edit_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton_sign = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sign.setGeometry(QtCore.QRect(460, 500, 100, 50))
        self.pushButton_sign.setObjectName("pushButton_sign")
        self.pushButton_sign.setStyleSheet('''
                                                    QPushButton{
                                                    color:white;
                                                    background:#4169E1;
                                                    border-radius:20px;                                                    
                                                    }
                                                    QPushButton:hover{background:#0000FF;}
                                                    ''')

        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(650, 500, 100, 50))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_exit.setStyleSheet('''
                                                            QPushButton{
                                                            color:white;
                                                            background:#F76677;
                                                            border-radius:20px;                                                            
                                                            }
                                                            QPushButton:hover{background:red;}
                                                            ''')
        # 标题
        self.label_t = QtWidgets.QLabel(self.centralwidget)
        self.label_t.setGeometry(QtCore.QRect(300, 100, 585, 100))
        self.label_t.setObjectName("label_t")
        self.label_t.setStyleSheet('''
                                    QLabel{background-color: transparent;
                                           border:none;
                                           font-size:50px;
                                           font-weight:1500;
                                           color:white;
                                           }                                
                                   ''')

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 1160, 470))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")


        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1160, 470))
        self.graphicsView.setObjectName("graphicsView")

        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(20, 520, 1160, 342))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")


        # 为登录界面隐藏这两个frame
        self.frame_3.setVisible(False)
        self.frame.setVisible(False)

        # 关闭按钮
        self.pushButton_close = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_close.setGeometry(QtCore.QRect(560, 280, 28, 28))
        self.pushButton_close.setObjectName("close")
        self.pushButton_close.setStyleSheet('''
                                            QPushButton{
                                            background:#F76677;
                                            border-radius:10px;
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:red;}
                                            ''')

        # 1.加载图像
        self.groupBox = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 511, 111))
        # self.groupBox.setStyleSheet("background:red")
        self.groupBox.setObjectName("groupBox")

        # 空格子中显示图像的路径
        self.textEdit_srcImg = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_srcImg.setGeometry(QtCore.QRect(10, 60, 500, 31))
        self.textEdit_srcImg.setObjectName("textEdit_srcImg")
        self.textEdit_srcImg.setStyleSheet("border:1px solid white;")
        # 按钮：浏览（加载图像下的浏览）
        self.pushButton_srcImg = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_srcImg.setGeometry(QtCore.QRect(170, 10, 200, 30))
        self.pushButton_srcImg.setObjectName("pushButton_srcImg")
        self.pushButton_srcImg.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')

        # 2.铭牌识别
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox_2.setGeometry(QtCore.QRect(640, 20, 511, 111))
        # self.groupBox_2.setStyleSheet("background:blur")
        self.groupBox_2.setObjectName("groupBox_2")
        # 按钮：开始识别
        self.pushButton_ocr = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_ocr.setGeometry(QtCore.QRect(10, 30, 491, 41))
        self.pushButton_ocr.setObjectName("pushButton_ocr")
        self.pushButton_ocr.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')
        # label：识别结果
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 80, 71, 31))
        self.label_5.setObjectName("label_5")
        # 空格子中识别结果显示
        self.textEdit_ocr = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_ocr.setGeometry(QtCore.QRect(90, 80, 421, 31))
        self.textEdit_ocr.setReadOnly(True)
        self.textEdit_ocr.setObjectName("textEdit_ocr")
        self.textEdit_ocr.setStyleSheet("border:1px solid white;")

        # 3.下载测量表
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 121, 511, 190))
        # self.groupBox_3.setStyleSheet("background:blur")
        self.groupBox_3.setObjectName("groupBox_3")
        # label：铭牌号码
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 71, 31))
        self.label_2.setObjectName("label_2")
        # 空格子中显示名牌号码
        self.textEdit_nameplate = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_nameplate.setGeometry(QtCore.QRect(90, 20, 311, 31))
        self.textEdit_nameplate.setReadOnly(True)
        self.textEdit_nameplate.setObjectName("textEdit_nameplate")
        self.textEdit_nameplate.setStyleSheet("border:1px solid white;")
        # 按钮：修改
        self.pushButton_nameplate_modify = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_nameplate_modify.setGeometry(QtCore.QRect(410, 20, 93, 31))
        self.pushButton_nameplate_modify.setObjectName("pushButton_nameplate_modify")
        self.pushButton_nameplate_modify.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')
        # label：下载地址
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 71, 31))
        self.label_3.setObjectName("label_3")
        # 空格子中显示下载的网址
        self.textEdit_download = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_download.setGeometry(QtCore.QRect(90, 60, 311, 31))
        self.textEdit_download.setText(HOST_URL_DOWN)
        self.textEdit_download.setReadOnly(True)
        self.textEdit_download.setObjectName("textEdit_download")
        self.textEdit_download.setStyleSheet("border:1px solid white;")
        # 按钮：下载
        self.pushButton_download_start = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download_start.setGeometry(QtCore.QRect(10, 140, 491, 31))
        self.pushButton_download_start.setObjectName("pushButton_download_start")
        self.pushButton_download_start.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')
        # 按钮：修改
        self.pushButton_download = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download.setGeometry(QtCore.QRect(410, 60, 93, 28))
        self.pushButton_download.setObjectName("pushButton_download")
        self.pushButton_download.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')
        # label：下载路径
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 71, 31))
        self.label_7.setObjectName("label_7")
        # 空格子中显示下载的路径
        self.textEdit_download_pc = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_download_pc.setGeometry(QtCore.QRect(90, 100, 311, 31))
        self.textEdit_download_pc.setReadOnly(True)
        self.textEdit_download_pc.setObjectName("textEdit_download_pc")
        self.textEdit_download_pc.setStyleSheet("border:1px solid white;")
        # 按钮：浏览
        self.pushButton_download_find = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download_find.setGeometry(QtCore.QRect(410, 100, 93, 28))
        self.pushButton_download_find.setObjectName("pushButton_download_find")
        self.pushButton_download_find.setStyleSheet('''
                                                    QPushButton{
                                                    border:1px solid white;
                                                    }
                                                    QPushButton:hover{background:#000000;}
                                                    ''')

        # 4.上传测量表
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox_4.setGeometry(QtCore.QRect(629, 151, 511, 141))
        # self.groupBox_4.setStyleSheet("background:blur")
        self.groupBox_4.setObjectName("groupBox_4")
        # label：上传路径
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 71, 31))
        self.label_4.setObjectName("label_4")
        # 空格子中显示上传路径
        self.textEdit_upload = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_upload.setGeometry(QtCore.QRect(90, 60, 311, 31))
        self.textEdit_upload.setObjectName("textEdit_upload")
        self.textEdit_upload.setStyleSheet("border:1px solid white;")
        # label：上传网址
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 71, 31))
        self.label_6.setObjectName("label_6")
        # 空格子中显示上传的网址
        self.textEdit_upload_url = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_upload_url.setGeometry(QtCore.QRect(90, 20, 311, 31))
        self.textEdit_upload_url.setText(HOST_URL_UPLOAD)
        self.textEdit_upload_url.setReadOnly(True)
        self.textEdit_upload_url.setObjectName("textEdit_upload_url")
        self.textEdit_upload_url.setStyleSheet("border:1px solid white;")
        # 按钮：修改
        self.pushButton_uoloadplate_modify = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_uoloadplate_modify.setGeometry(QtCore.QRect(410, 20, 93, 31))
        self.pushButton_uoloadplate_modify.setObjectName("pushButton_nameplate_modify")
        self.pushButton_uoloadplate_modify.setStyleSheet('''
                                                    QPushButton{
                                                    border:1px solid white;
                                                    }
                                                    QPushButton:hover{background:#000000;}
                                                    ''')
        # 按钮：上传
        self.pushButton_upload_start = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_upload_start.setGeometry(QtCore.QRect(10, 100, 491, 31))
        self.pushButton_upload_start.setObjectName("pushButton_upload_start")
        self.pushButton_upload_start.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')
        # 按钮：浏览
        self.pushButton_upload = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_upload.setGeometry(QtCore.QRect(410, 60, 93, 28))
        self.pushButton_upload.setObjectName("pushButton_upload")
        self.pushButton_upload.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            }
                                            QPushButton:hover{background:#000000;}
                                            ''')


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)




        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 美化
        # 主界面（子界面会继承属性）
        MainWindow.setStyleSheet('''
                                background:white;
                                border-top:1px solid darkGray;
                                border-bottom:1px solid darkGray;
                                border-right:1px solid darkGray;
                                border-top-right-radius:10px;
                                border-top-left-radius:10px;
                                border-bottom-right-radius:10px;
                                border-bottom-left-radius:10px;
                                font-size:16px;
                                font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                ''')

        # 登陆界面

        # 下半部分
        self.frame_3.setStyleSheet('''
                                    background:#696969;
                                    border:none;     
                                    color:white; 
                                    QPushButton{
                                    font-size:17px;
                                    font-weight:700;
                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                    '''
                                   )
        # 视图
        self.frame.setStyleSheet('''
                                    background:#D3D3D3;
                                ''')


        # 透明度
        MainWindow.setWindowOpacity(0.9)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 隐藏边框
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "铭牌识别系统"))
        self.groupBox.setTitle(_translate("MainWindow", "1 连接扫描仪"))
        self.pushButton_srcImg.setText(_translate("MainWindow", "重启服务器"))

        self.groupBox_2.setTitle(_translate("MainWindow", "2 铭牌识别"))
        self.pushButton_ocr.setText(_translate("MainWindow", "再次识别"))
        self.label_5.setText(_translate("MainWindow", "识别结果"))
        self.groupBox_3.setTitle(_translate("MainWindow", "3 下载测量表"))
        self.label_2.setText(_translate("MainWindow", "铭牌号码"))
        self.pushButton_nameplate_modify.setText(_translate("MainWindow", "修改"))
        self.label_3.setText(_translate("MainWindow", "下载地址"))
        self.pushButton_download_start.setText(_translate("MainWindow", "下载"))
        self.pushButton_download.setText(_translate("MainWindow", "修改"))
        self.groupBox_4.setTitle(_translate("MainWindow", "4 上传测量表"))
        self.label_4.setText(_translate("MainWindow", "选择文件"))
        self.pushButton_upload_start.setText(_translate("MainWindow", "上传"))
        self.pushButton_upload.setText(_translate("MainWindow", "浏览"))
        self.pushButton_uoloadplate_modify.setText(_translate("MainWindow", "修改"))
        self.label_6.setText((_translate("MainWindow", "上传网址")))
        self.label_7.setText((_translate("MainWindow", "下载路径")))
        self.pushButton_download_find.setText((_translate("MainWindow", "浏览")))
        self.pushButton_close.setText(_translate("MainWindow", " "))
        self.pushButton_sign.setText(_translate("MainWindow", "登  录"))
        self.pushButton_exit.setText(_translate("MainWindow", "退  出"))
        self.label_t.setText((_translate("MainWindow", "       铭 牌 识 别 系 统")))
