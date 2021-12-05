import os
from tkinter import *
from tkinter.messagebox import showinfo, showerror

import requests
import windnd

LOG_LINE_NUM = 0
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400
URL = "https://source.unsplash.com/random"
PACK2IMG = [".rar", ".zip", ".jar", ".tar", ".7z", ".tgz"]
IMG2PACK = [".jpg", ".png"]


class PicMerger():

    def __init__(self) -> None:
        self.app = Tk()

    def set_attr(self):
        self.app.title("图片合成工具V1.0.0")
        self.app.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, self.app.winfo_screenwidth() // 2,
                                               (self.app.winfo_screenheight() - WINDOW_HEIGHT) // 2))
        # self.app.resizable(False, False)
        self.app.config(background="SkyBlue")
        self.app.iconbitmap("./icon.ico")

    def set_wgt(self):
        info_msg = Label(self.app, text="请将需要分享的压缩包或需要恢复的文件拖到这里\n"
                                        "Please drag and drop your files here",
                         font=("courier", 14, "bold"), background="SkyBlue", foreground="FireBrick")
        author_info = Label(self.app, text="By ThunStorm", font=("courier", 10, "bold"), cursor="circle")
        info_msg.pack(side="top", expand=1)
        author_info.pack(side="bottom", fill="x", anchor="se")

    def set_func(self):
        windnd.hook_dropfiles(self.app, func=self.file_process)

    def file_process(self, files):
        if not self.download_pic():
            return
        fileList = [file.decode('gbk') for file in files]
        print(fileList)
        for file in fileList:
            path, filename = os.path.split(file)
            filename, extension = os.path.splitext(filename)
            print("path={}, filename={}, ext={}".format(path, filename, extension))
            if extension in PACK2IMG:
                self.generate_img(file, path, filename, extension)
            elif extension in IMG2PACK:
                self.recover_arch(file, path, filename)
        showinfo("完成", "任务完成")
        os.remove("cover.jpg")

    def download_pic(self):
        try:
            imgPage = requests.get(URL, stream=True)
            img_name = "cover.jpg"
            with open(img_name, "wb") as f:
                f.write(imgPage.content)
            return True
        except Exception:
            error_msg = "请检查网络并重试\nPlease check your network connection"
            showerror("爬取失败", error_msg)
            return False

    def generate_img(self, file, path, filename, ext):
        status = os.system("copy /b .\\cover.jpg+{} {}\\{}_{}.jpg".format(file, path, ext[1:], filename))
        if status != 0:
            showerror("错误", "出现错误，请重试！")

    def recover_arch(self, file, path, filename):
        index = 0 if filename.find("_") == -1 else filename.find("_")
        print("copy {} {}\\{}.{}".format(file, path, filename[index + 1:], filename[:index]))
        status = os.system("copy {} {}\\{}.{}".format(file, path, filename[index + 1:], filename[:index]))
        if status != 0:
            showerror("错误", "出现错误，请重试！")

    def run(self):
        self.set_attr()
        self.set_wgt()
        self.set_func()
        self.app.mainloop()


app = PicMerger()
app.run()
