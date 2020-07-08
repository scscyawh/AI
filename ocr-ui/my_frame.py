from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage

HOST_URL_DOWN = 'http://192.168.3.63:8080/upload/selectFastUploadUrl?nameplateId='
HOST_URL_UPLOAD = 'http://192.168.3.63:8080/upload/fastFinsihUploadFile'
SUPPLIER_URL_DOWN = 'http://192.168.3.63:8088/SupplierUpload/selectFastUploadUrl?nameplateId='
SUPPLIER_URL_UPLOAD = 'http://192.168.3.63:8088/SupplierUpload/fastFinsihUploadFile'
HOST = '192.168.3.145'  # "192.168.0.102"
PORT = 8888


def changeOpacity(myshow, change=0.5):
    op = QtWidgets.QGraphicsOpacityEffect()
    op.setOpacity(change)
    myshow.setGraphicsEffect(op)
    myshow.setAutoFillBackground(True)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 830)
        MainWindow.setFixedSize(1600, 830)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 背景图层
        self.frame_background = QtWidgets.QFrame(self.centralwidget)
        self.frame_background.setGeometry(QtCore.QRect(0, 0, 1600, 800))
        self.frame_background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_background.setObjectName("frame_background")
        self.frame_background.setStyleSheet('''        
                                         background:white;  
                                         border-radius:80px;                   
                                      ''')

        # 登录界面背景图层
        self.frame_sign = QtWidgets.QFrame(self.centralwidget)
        self.frame_sign.setGeometry(QtCore.QRect(0, 0, 1600, 800))
        self.frame_sign.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sign.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sign.setObjectName("frame_sign")
        self.frame_sign.setStyleSheet('''                                
                                         border-top-right-radius:5px;
                                         border-top-left-radius:5px;
                                         border-bottom-left-radius:5px;
                                         border-bottom-right-radius:5px;
                                         border-image:url(71.jpg);  
                                      ''')
        # 设置按钮
        self.pushButton_setting = QtWidgets.QPushButton(self.frame_sign)
        self.pushButton_setting.setGeometry(QtCore.QRect(20, 20, 120, 100))
        self.pushButton_setting.setObjectName('pushButton_setting')
        self.pushButton_setting.setStyleSheet('border-image:url(setting.png);')

        # create
        self.GraphicsView_create = QtWidgets.QGraphicsView(self.frame_sign)
        self.GraphicsView_create.setGeometry(QtCore.QRect(630, -25, 350, 350))
        self.GraphicsView_create.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GraphicsView_create.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GraphicsView_create.setObjectName("GraphicsView_create")
        self.GraphicsView_create.setStyleSheet("border-image:url(create.png);")

        self.Edit_sign = QtWidgets.QTextEdit(self.centralwidget)
        self.Edit_sign.setGeometry(QtCore.QRect(620, 350, 350, 35))
        self.Edit_sign.setObjectName("Edit_sign")
        self.Edit_sign.setPlaceholderText("username")
        self.Edit_sign.setStyleSheet('''
                                      color:white;
                                      background:#000000;
                                      border-radius:2px;
                                      border-bottom:1px solid white;
                                      border-right:1px solid white;
                                     ''')

        self.Edit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.Edit_password.setGeometry(QtCore.QRect(620, 430, 350, 35))
        self.Edit_password.setObjectName("Edit_password")
        self.Edit_password.setPlaceholderText("password")
        self.Edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Edit_password.setStyleSheet('''
                                              color:white;
                                              background:#000000;
                                              border-radius:2px;
                                              border-bottom:1px solid white;
                                              border-right:1px solid white;
                                             ''')

        self.pushButton_sign = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sign.setGeometry(QtCore.QRect(670, 520, 250, 35))
        self.pushButton_sign.setObjectName("pushButton_sign")
        self.pushButton_sign.setStyleSheet('''
                                                    QPushButton{
                                                    color:white;
                                                    background:#000000;
                                                    border-radius:2px; 	
                                                    border-bottom:1px solid white;
                                                    border-right:1px solid white;                                                  
                                                    }
                                                    QPushButton:hover{background:#808080;}
                                                    ''')
        changeOpacity(self.Edit_sign)
        changeOpacity(self.Edit_password)
        changeOpacity(self.pushButton_sign)

        # 登录界面的exit
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(745, 620, 100, 100))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_exit.setStyleSheet('''
                                                            QPushButton{
                                                            color:white;
                                                            border-image:url(exit2.png);
                                                            border-radius:20px;
                                                            }
                                                            QPushButton:hover{background:#808080;}
                                                            ''')
        changeOpacity(self.pushButton_exit, 0.7)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(612, 0, 988, 800))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 988, 800))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet('border-radius:80px;')

        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 612, 800))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        # 为登录界面隐藏这两个frame
        self.frame_3.setVisible(False)
        self.frame.setVisible(False)

        # 关闭按钮
        self.pushButton_close = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_close.setGeometry(QtCore.QRect(538, 30, 60, 50))
        self.pushButton_close.setObjectName("close")
        self.pushButton_close.setStyleSheet('''
                                            QPushButton{
                                            border-radius:10px;
                                            border:1px solid white;
                                            border-image:url(exit.png);
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')

        # 最小化按钮
        self.pushButton_Min = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_Min.setGeometry(QtCore.QRect(44, 30, 60, 50))
        self.pushButton_Min.setObjectName("Min")
        self.pushButton_Min.setStyleSheet('''
                                                    QPushButton{
                                                    border-radius:10px;
                                                    border:1px solid white;
                                                    border-image:url(I.png);
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')

        # 1.连接扫描仪
        self.groupBox = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox.setGeometry(QtCore.QRect(20, 100, 612, 700))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("border:none;")
        # label:连接扫描仪
        self.title_saomao = QtWidgets.QLabel(self.groupBox)
        self.title_saomao.setObjectName("title_saomao")
        self.title_saomao.setGeometry(QtCore.QRect(210, 10, 200, 60))
        self.title_saomao.setText("连接扫描仪")
        self.title_saomao.setStyleSheet('''
                                        font-size:25px;
                                        font-weight:1000;
                                        ''')
        # label：服务器IP
        self.label_IP = QtWidgets.QLabel(self.groupBox)
        self.label_IP.setGeometry(QtCore.QRect(10, 110, 71, 31))
        self.label_IP.setObjectName("label_IP")
        self.label_IP.setText('IP')
        # 服务器IP显示
        self.textEdit_IP = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_IP.setGeometry(QtCore.QRect(150, 110, 421, 40))
        self.textEdit_IP.setObjectName("textEdit_IP")
        self.textEdit_IP.setText(HOST)
        self.textEdit_IP.setStyleSheet('color:#808080')
        # label：端口号
        self.label_PORT = QtWidgets.QLabel(self.groupBox)
        self.label_PORT.setGeometry(QtCore.QRect(10, 150, 71, 31))
        self.label_PORT.setObjectName("label_PORT")
        self.label_PORT.setText('端口号')
        # 端口号显示
        self.textEdit_PORT = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_PORT.setGeometry(QtCore.QRect(150, 150, 421, 40))
        self.textEdit_PORT.setText(str(PORT))
        self.textEdit_PORT.setObjectName("textEdit_PORT")
        self.textEdit_PORT.setStyleSheet('color:#808080')
        # label：温馨提示
        self.label_information = QtWidgets.QLabel(self.groupBox)
        self.label_information.setGeometry(QtCore.QRect(10, 190, 350, 31))
        self.label_information.setObjectName("label_information")
        self.label_information.setText('温馨提示-修改IP和端口号后需要重启服务器')
        self.label_information.setStyleSheet('color:#808080')
        # 显示服务器状态
        self.textEdit_srcImg = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_srcImg.setGeometry(QtCore.QRect(10, 260, 350, 80))
        self.textEdit_srcImg.setObjectName("textEdit_srcImg")
        self.textEdit_srcImg.setReadOnly(True)
        # 按钮：重启服务器
        self.pushButton_srcImg = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_srcImg.setGeometry(QtCore.QRect(370, 260, 200, 30))
        self.pushButton_srcImg.setObjectName("pushButton_srcImg")
        self.pushButton_srcImg.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        # label：识别结果
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 410, 71, 31))
        self.label_5.setObjectName("label_5")

        # 空格子中识别结果显示
        self.textEdit_ocr = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_ocr.setGeometry(QtCore.QRect(150, 410, 421, 40))
        self.textEdit_ocr.setReadOnly(True)
        self.textEdit_ocr.setObjectName("textEdit_ocr")
        self.textEdit_ocr.setStyleSheet('color:#808080')
        # label：时间
        self.label_cost = QtWidgets.QLabel(self.groupBox)
        self.label_cost.setGeometry(QtCore.QRect(10, 450, 71, 31))
        self.label_cost.setObjectName("label_cost")
        self.label_cost.setText('识别耗时')

        # 时间
        self.textEdit_cost = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_cost.setGeometry(QtCore.QRect(150, 450, 421, 40))
        self.textEdit_cost.setReadOnly(True)
        self.textEdit_cost.setObjectName("textEdit_cost")
        self.textEdit_cost.setStyleSheet('color:#808080')

        # 3.主机厂
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 100, 612, 700))
        # self.groupBox_3.setStyleSheet("background:blur")
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setStyleSheet('''
                                        border:none;
                                      '''
                                      )
        # 按钮：选择上传或者下载
        self.HOST_PUSHDOWN = QtWidgets.QPushButton(self.groupBox_3)
        self.HOST_PUSHDOWN.setGeometry(QtCore.QRect(335, 470, 102, 80))
        self.HOST_PUSHDOWN.setObjectName("HOST_PUSHDOWN")
        self.HOST_PUSHDOWN.setStyleSheet('''
                                            QPushButton{
                                            border:1px solid white;
                                            border-radius:20px;
                                            border-image:url(next.png);
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')

        # label:主机厂
        self.title_host = QtWidgets.QLabel(self.groupBox_3)
        self.title_host.setObjectName("title_host")
        self.title_host.setGeometry(QtCore.QRect(210, 10, 200, 60))
        self.title_host.setText("主  机  厂")
        self.title_host.setStyleSheet('''
                                        font-size:25px;
                                        font-weight:1000;
                                      ''')
        # label：识别结果
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 71, 31))
        self.label_2.setObjectName("label_2")
        # 显示识别结果
        self.textEdit_nameplate = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_nameplate.setGeometry(QtCore.QRect(90, 110, 400, 40))
        self.textEdit_nameplate.setReadOnly(True)
        self.textEdit_nameplate.setObjectName("textEdit_nameplate")
        self.textEdit_nameplate.setStyleSheet('color:#808080')

        # 按钮：修改
        self.pushButton_nameplate_modify = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_nameplate_modify.setGeometry(QtCore.QRect(492, 110, 93, 31))
        self.pushButton_nameplate_modify.setObjectName("pushButton_nameplate_modify")
        self.pushButton_nameplate_modify.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        '''
        主机厂:下载
        '''
        # label：下载地址
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 250, 71, 31))
        self.label_3.setObjectName("label_3")
        # 空格子中显示下载的网址
        self.textEdit_download = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_download.setGeometry(QtCore.QRect(90, 250, 400, 60))
        self.textEdit_download.setText(HOST_URL_DOWN)
        self.textEdit_download.setReadOnly(True)
        self.textEdit_download.setObjectName("textEdit_download")
        self.textEdit_download.setStyleSheet('color:#808080')
        # 按钮：修改
        self.pushButton_download = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download.setGeometry(QtCore.QRect(492, 250, 93, 31))
        self.pushButton_download.setObjectName("pushButton_download")
        self.pushButton_download.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        # label：下载路径
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 400, 71, 31))
        self.label_7.setObjectName("label_7")
        # 空格子中显示下载的路径
        self.textEdit_download_pc = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_download_pc.setGeometry(QtCore.QRect(90, 400, 400, 60))
        self.textEdit_download_pc.setReadOnly(True)
        self.textEdit_download_pc.setObjectName("textEdit_download_pc")
        self.textEdit_download_pc.setStyleSheet('color:#808080')

        # 按钮：浏览
        self.pushButton_download_find = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download_find.setGeometry(QtCore.QRect(492, 400, 93, 31))
        self.pushButton_download_find.setObjectName("pushButton_download_find")
        self.pushButton_download_find.setStyleSheet('''
                                                    QPushButton{
                                                    border:2px solid black;
                                                    border-radius:10px;
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')
        # 按钮：下载
        self.pushButton_download_start = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_download_start.setGeometry(QtCore.QRect(110, 470, 102, 80))
        self.pushButton_download_start.setObjectName("pushButton_download_start")
        self.pushButton_download_start.setStyleSheet('''
                                            QPushButton{
                                            border-radius:15px;
                                            border-image:url(down.png);
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        '''
        主机厂:上传
        '''
        # label：上传地址
        self.label_host_upload = QtWidgets.QLabel(self.groupBox_3)
        self.label_host_upload.setGeometry(QtCore.QRect(10, 250, 71, 31))
        self.label_host_upload.setObjectName("label_host_upload")
        self.label_host_upload.setText("上传地址")
        self.label_host_upload.setVisible(False)
        # 空格子中显示上传的网址
        self.textEdit_host_upload = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_host_upload.setGeometry(QtCore.QRect(90, 250, 400, 60))
        self.textEdit_host_upload.setText(HOST_URL_UPLOAD)
        self.textEdit_host_upload.setReadOnly(True)
        self.textEdit_host_upload.setObjectName("textEdit_host_upload")
        self.textEdit_host_upload.setVisible(False)
        self.textEdit_host_upload.setStyleSheet('color:#808080')


        # 按钮：修改
        self.pushButton_host_upload_modify = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_host_upload_modify.setVisible(False)
        self.pushButton_host_upload_modify.setGeometry(QtCore.QRect(492, 250, 93, 31))
        self.pushButton_host_upload_modify.setObjectName("pushButton_host_upload_modify")
        self.pushButton_host_upload_modify.setText('修改')
        self.pushButton_host_upload_modify.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        # label：文件路径
        self.label_host_upfile = QtWidgets.QLabel(self.groupBox_3)
        self.label_host_upfile.setGeometry(QtCore.QRect(10, 400, 71, 31))
        self.label_host_upfile.setObjectName("label_host_upfile")
        self.label_host_upfile.setText('文件路径')
        self.label_host_upfile.setVisible(False)

        # 文件的路径
        self.textEdit_host_upfile = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_host_upfile.setGeometry(QtCore.QRect(90, 400, 400, 60))
        self.textEdit_host_upfile.setReadOnly(True)
        self.textEdit_host_upfile.setObjectName("textEdit_host_upfile")
        self.textEdit_host_upfile.setVisible(False)
        self.textEdit_host_upfile.setStyleSheet('color:#808080')


        # 按钮：浏览
        self.pushButton_host_upfile = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_host_upfile.setVisible(False)
        self.pushButton_host_upfile.setGeometry(QtCore.QRect(492, 400, 93, 31))
        self.pushButton_host_upfile.setObjectName("pushButton_host_upfile")
        self.pushButton_host_upfile.setText('浏览')
        self.pushButton_host_upfile.setStyleSheet('''
                                                    QPushButton{
                                                    border:2px solid black;
                                                    border-radius:10px;
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')
        # 按钮：上传
        self.pushButton_host_upstart = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_host_upstart.setGeometry(QtCore.QRect(110, 470, 102, 80))
        self.pushButton_host_upstart.setObjectName("pushButton_host_upstart")
        self.pushButton_host_upstart.setVisible(False)
        self.pushButton_host_upstart.setStyleSheet('''
                                            QPushButton{
                                            border-image:url(up.png);
                                            border-radius:15px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')

        # 4.供应商
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame_3)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 100, 612, 700))
        self.groupBox_4.setObjectName("groupBox_4")
        # 按钮：选择上传或者下载
        self.SUPPLY_PUSHDOWN = QtWidgets.QPushButton(self.groupBox_4)
        self.SUPPLY_PUSHDOWN.setGeometry(QtCore.QRect(335, 470, 102, 80))
        self.SUPPLY_PUSHDOWN.setObjectName("SUPPLY_PUSHDOWN")
        self.SUPPLY_PUSHDOWN.setStyleSheet('''
                                                    QPushButton{
                                                    border:1px solid white;
                                                    border-radius:20px;
                                                    border-image:url(next.png);
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')
        # label:供应商
        self.title_supply = QtWidgets.QLabel(self.groupBox_4)
        self.title_supply.setObjectName("title_supply")
        self.title_supply.setGeometry(QtCore.QRect(210, 10, 200, 60))
        self.title_supply.setText("供  应  商")
        self.title_supply.setStyleSheet('''
                                        border:none;
                                        font-size:25px;
                                        font-weight:1000;
                                      ''')
        # label：识别结果
        self.label_2_su = QtWidgets.QLabel(self.groupBox_4)
        self.label_2_su.setGeometry(QtCore.QRect(10, 110, 71, 31))
        self.label_2_su.setObjectName("label_2_su")
        self.label_2_su.setText('识别结果')
        # 显示识别结果
        self.textEdit_nameplate_su = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_nameplate_su.setGeometry(QtCore.QRect(90, 110, 400, 40))
        self.textEdit_nameplate_su.setReadOnly(True)
        self.textEdit_nameplate_su.setObjectName("textEdit_nameplate_su")
        self.textEdit_nameplate_su.setStyleSheet("")
        self.textEdit_nameplate_su.setStyleSheet('color:#808080')

        # 按钮：修改
        self.pushButton_nameplate_modify_su = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_nameplate_modify_su.setGeometry(QtCore.QRect(492, 110, 93, 31))
        self.pushButton_nameplate_modify_su.setObjectName("pushButton_nameplate_modify_su")
        self.pushButton_nameplate_modify_su.setText('修改')
        self.pushButton_nameplate_modify_su.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        '''
        供应商:下载
        '''
        # label：下载地址
        self.label_3_su = QtWidgets.QLabel(self.groupBox_4)
        self.label_3_su.setGeometry(QtCore.QRect(10, 250, 71, 31))
        self.label_3_su.setObjectName("label_3")
        self.label_3_su.setText('下载地址')
        # 空格子中显示下载的网址
        self.textEdit_download_su = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_download_su.setGeometry(QtCore.QRect(90, 250, 400, 60))
        self.textEdit_download_su.setText(SUPPLIER_URL_DOWN)
        self.textEdit_download_su.setReadOnly(True)
        self.textEdit_download_su.setObjectName("textEdit_download_su")
        self.textEdit_download_su.setStyleSheet('color:#808080')

        # 按钮：修改
        self.pushButton_download_su = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_download_su.setGeometry(QtCore.QRect(492, 250, 93, 31))
        self.pushButton_download_su.setObjectName("pushButton_download_su")
        self.pushButton_download_su.setText('修改')
        self.pushButton_download_su.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        # label：下载路径
        self.label_7_su = QtWidgets.QLabel(self.groupBox_4)
        self.label_7_su.setGeometry(QtCore.QRect(10, 400, 71, 31))
        self.label_7_su.setObjectName("label_7")
        self.label_7_su.setText('下载路径')
        # 空格子中显示下载的路径
        self.textEdit_download_pc_su = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_download_pc_su.setGeometry(QtCore.QRect(90, 400, 400, 60))
        self.textEdit_download_pc_su.setReadOnly(True)
        self.textEdit_download_pc_su.setObjectName("textEdit_download_pc_su")
        self.textEdit_download_pc_su.setStyleSheet('color:#808080')

        # 按钮：浏览
        self.pushButton_download_find_su = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_download_find_su.setGeometry(QtCore.QRect(492, 400, 93, 31))
        self.pushButton_download_find_su.setObjectName("pushButton_download_find_su")
        self.pushButton_download_find_su.setText('浏览')
        self.pushButton_download_find_su.setStyleSheet('''
                                                    QPushButton{
                                                    border:2px solid black;
                                                    border-radius:10px;
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')
        # 按钮：下载
        self.pushButton_download_start_su = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_download_start_su.setGeometry(QtCore.QRect(110, 470, 102, 80))
        self.pushButton_download_start_su.setObjectName("pushButton_download_start_su")
        self.pushButton_download_start_su.setStyleSheet('''
                                            QPushButton{
                                            border-image:url(down.png);
                                            border-radius:15px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        '''
        供应商:上传
        '''
        # label：上传地址
        self.label_supply_upload = QtWidgets.QLabel(self.groupBox_4)
        self.label_supply_upload.setGeometry(QtCore.QRect(10, 250, 71, 31))
        self.label_supply_upload.setObjectName("label_supply_upload")
        self.label_supply_upload.setText("上传地址")
        self.label_supply_upload.setVisible(False)
        # 空格子中显示上传的网址
        self.textEdit_supply_upload = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_supply_upload.setVisible(False)
        self.textEdit_supply_upload.setGeometry(QtCore.QRect(90, 250, 400, 60))
        self.textEdit_supply_upload.setText(SUPPLIER_URL_UPLOAD)
        self.textEdit_supply_upload.setReadOnly(True)
        self.textEdit_supply_upload.setObjectName("textEdit_supply_upload")
        self.textEdit_supply_upload.setStyleSheet('color:#808080')

        # 按钮：修改
        self.pushButton_supply_upload_modify = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_supply_upload_modify.setVisible(False)
        self.pushButton_supply_upload_modify.setGeometry(QtCore.QRect(492, 250, 93, 31))
        self.pushButton_supply_upload_modify.setObjectName("pushButton_supply_upload_modify")
        self.pushButton_supply_upload_modify.setText('修改')
        self.pushButton_supply_upload_modify.setStyleSheet('''
                                            QPushButton{
                                            border:2px solid black;
                                            border-radius:10px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')
        # label：文件路径
        self.label_supply_upfile = QtWidgets.QLabel(self.groupBox_4)
        self.label_supply_upfile.setGeometry(QtCore.QRect(10, 400, 71, 31))
        self.label_supply_upfile.setObjectName("label_supply_upfile")
        self.label_supply_upfile.setText('文件路径')
        self.label_supply_upfile.setVisible(False)
        # 文件的路径
        self.textEdit_supply_upfile = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_supply_upfile.setGeometry(QtCore.QRect(90, 400, 400, 60))
        self.textEdit_supply_upfile.setReadOnly(True)
        self.textEdit_supply_upfile.setObjectName("textEdit_supply_upfile")
        self.textEdit_supply_upfile.setVisible(False)
        self.textEdit_supply_upfile.setStyleSheet('color:#808080')

        # 按钮：浏览
        self.pushButton_supply_upfile = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_supply_upfile.setVisible(False)
        self.pushButton_supply_upfile.setGeometry(QtCore.QRect(492, 400, 93, 31))
        self.pushButton_supply_upfile.setObjectName("pushButton_supply_upfile")
        self.pushButton_supply_upfile.setText('浏览')
        self.pushButton_supply_upfile.setStyleSheet('''
                                                    QPushButton{
                                                    border:2px solid black;
                                                    border-radius:10px;
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')
        # 按钮：上传
        self.pushButton_supply_upstart = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_supply_upstart.setVisible(False)
        self.pushButton_supply_upstart.setGeometry(QtCore.QRect(110, 470, 102, 80))
        self.pushButton_supply_upstart.setObjectName("pushButton_supply_upstart")
        self.pushButton_supply_upstart.setStyleSheet('''
                                            QPushButton{
                                            border-image:url(up.png);
                                            border-radius:15px;
                                            }
                                            QPushButton:hover{background:#DCDCDC;}
                                            ''')

        '''
        7.1日界面大改
        '''
        # 为三个按钮做准备，隐藏组件
        self.groupBox.setVisible(True)
        self.groupBox_3.setVisible(False)
        self.groupBox_4.setVisible(False)

        # 切换按钮：扫描仪
        self.change_analysis = QtWidgets.QPushButton(self.frame_3)
        self.change_analysis.setGeometry(QtCore.QRect(40, 678, 102, 80))
        self.change_analysis.setObjectName("change_analysis")
        self.change_analysis.setStyleSheet('''
                                                    QPushButton{
                                                    border:1px solid white;
                                                    border-radius:20px;
                                                    border-image:url(saomiaoyi.png);
                                                    }
                                                    QPushButton:hover{background:#DCDCDC;}
                                                    ''')

        # 切换按钮：主机厂
        self.change_host = QtWidgets.QPushButton(self.frame_3)
        self.change_host.setGeometry(QtCore.QRect(244, 678, 102, 80))
        self.change_host.setObjectName("change_host")
        self.change_host.setStyleSheet('''
                                                           QPushButton{
                                                           border:1px solid white;
                                                           border-radius:20px;
                                                           border-image:url(host.png);
                                                           }
                                                           QPushButton:hover{background:#DCDCDC;}
                                                           ''')
        # 切换按钮：供应商
        self.change_supply = QtWidgets.QPushButton(self.frame_3)
        self.change_supply.setGeometry(QtCore.QRect(448, 678, 102, 80))
        self.change_supply.setObjectName("change_supply")
        self.change_supply.setStyleSheet('''
                                                           QPushButton{
                                                           border:1px solid white;
                                                           border-radius:20px;
                                                           border-image:url(supply.png);
                                                           }
                                                           QPushButton:hover{background:#DCDCDC;}
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
                                font-size:16px;
                                font-weight:700;
                                font-family: "Microsoft YaHei";
                                ''')

        # 左半部分
        self.frame_3.setStyleSheet('''
                                    background:white;
                                    border:none;     
                                    color:black; 
                                    border-top-left-radius:80px;
                                    border-bottom-left-radius:80px;
                                    '''
                                   )
        # 视图
        self.frame.setStyleSheet('''
                                    background:black;
                                    border-radius:80px;
                                ''')

        # 透明度
        MainWindow.setWindowOpacity(0.9)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 隐藏边框
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "铭牌识别系统"))
        self.pushButton_srcImg.setText(_translate("MainWindow", "重启服务器"))

        self.label_5.setText(_translate("MainWindow", "识别结果"))
        self.label_2.setText(_translate("MainWindow", "识别结果"))
        self.pushButton_nameplate_modify.setText(_translate("MainWindow", "修改"))
        self.label_3.setText(_translate("MainWindow", "下载地址"))
        self.pushButton_download.setText(_translate("MainWindow", "修改"))
        self.label_7.setText((_translate("MainWindow", "下载路径")))
        self.pushButton_download_find.setText((_translate("MainWindow", "浏览")))
        self.pushButton_close.setText(_translate("MainWindow", " "))
        self.pushButton_Min.setText(_translate("MainWindow", " "))
        self.pushButton_sign.setText(_translate("MainWindow", "Sign   Up"))
        self.pushButton_exit.setText(_translate("MainWindow", ""))
