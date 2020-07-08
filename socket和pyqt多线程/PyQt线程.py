from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import time


class TestWindow(QDialog):
    def __init__(self):
        super().__init__()

        btn1 = QPushButton("Start", self)
        btn2 = QPushButton("Stop", self)
        self.sec_label = QLabel(self)

        layout = QGridLayout(self)
        layout.addWidget(btn1, 0, 0)
        layout.addWidget(btn2, 0, 1)
        layout.addWidget(self.sec_label, 1, 0, 1, 2)

        thread = MyThread()  # 创建一个线程
        thread.sec_changed_signal.connect(self.update)  # 线程发过来的信号挂接到槽：update
        btn1.clicked.connect(lambda: thread.start())
        btn2.clicked.connect(lambda: thread.terminate())  # 线程中止

    def update(self, data):
        self.sec_label.setText(str(data))


class MyThread(QThread):
    sec_changed_signal = pyqtSignal(int)  # 信号类型

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(10000):
            self.sec_changed_signal.emit(i)
            time.sleep(1)


app = QApplication(sys.argv)
form = TestWindow()
form.show()
app.exec_()
