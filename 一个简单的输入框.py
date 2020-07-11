from tkinter import *
import tkinter.messagebox


def getInput(title, message):
    def return_callback(event):
        root.quit()

    def close_callback():
        tkinter.messagebox.showinfo('提示', '确定退出？')
        str = None
        root.quit()

    root = Tk(className=title)
    root.wm_attributes('-topmost', 1)
    screenwidth, screenheight = root.maxsize()
    width = 300
    height = 100
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
    root.resizable(0, 0)
    lable = Label(root, height=2)
    lable['text'] = message
    lable.pack()
    entry = Entry(root)
    entry.bind('<Return>', return_callback)
    entry.pack()
    entry.focus_set()
    root.protocol("WM_DELETE_WINDOW", close_callback)
    root.mainloop()
    str = entry.get()
    root.destroy()
    return str


a = getInput('测试', '测试内容')
if a:
    print('ok')
else:
    print('no')
