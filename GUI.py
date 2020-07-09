from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from draw import draw_moving_car,draw_map
from Fuzzy_Compute import main_run
from DataPoint import *
import os

dir = '.\data'

# from kernal import get_gui_setting,drawpicture
class skin():
    def __init__(self):
        self.org_canvas = Canvas(window, width=600, height=600)
        self.img = PhotoImage(file='')
        self.imgArea = self.org_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.org_canvas.place(x=500, y=10, anchor='nw')
        # for data in os.listdir(dir):
        #     self.file.append(data)
        Label(window, text='Setting', font=('Arial', 12)).place(x=10, y=0)

        self.comboExample = ttk.Combobox(window,
                                         values=["case01.txt", "case02.txt","case03.txt"], font=('Arial', 10))
        self.comboExample.place(x=10, y=50)
        self.comboExample.current(0)

        self.comboway = ttk.Combobox(window,
                                         values=["最大平均法", "離散重心法"], font=('Arial', 10))
        self.comboway.place(x=10, y=80)
        self.comboway.current(0)

        Label(window, text='forward large mean and variance,use , to split:', font=('Arial', 8)).place(x=10, y=100)
        Label(window, text='forward medium mean and variance,use , to split:', font=('Arial', 8)).place(x=10, y=130)
        Label(window, text='forward small mean and variance,use , to split:', font=('Arial', 8)).place(x=10, y=160)
        Label(window, text='L-R distance large mean and variance,use , to split ', font=('Arial', 8)).place(x=10, y=190)
        Label(window, text='L-R distance medium mean and variance,use , to split :', font=('Arial', 8)).place(x=10, y=220)
        Label(window, text='L-R distance small mean and variance,use , to split :', font=('Arial', 8)).place(x=10, y=250)
        Label(window, text='theta degree large mean and variance,use , to split ', font=('Arial', 8)).place(x=10, y=280)
        Label(window, text='theta degree medium mean and variance,use , to split :', font=('Arial', 8)).place(x=10,y=310)
        Label(window, text='theta degree small mean and variance,use , to split :', font=('Arial', 8)).place(x=10,y=340)

        f_Large = StringVar()
        f_Large.set('18,5')
        f_Large_setting = Entry(window, textvariable=f_Large, font=('Arial', 10))
        f_Large_setting.place(x=300, y=100)

        f_medium = StringVar()
        f_medium.set('6,5')
        f_medium_setting = Entry(window, textvariable=f_medium, font=('Arial', 10))
        f_medium_setting.place(x=300, y=130)

        f_small = StringVar()
        f_small.set('3,10')
        f_small_setting = Entry(window, textvariable=f_small, font=('Arial', 10))
        f_small_setting.place(x=300, y=160)

        lr_large= StringVar()
        lr_large.set('3,2')
        lr_large_setting = Entry(window, textvariable=lr_large, font=('Arial', 10))
        lr_large_setting.place(x=300, y=190)

        lr_mediun = StringVar()
        lr_mediun.set('0,3')
        lr_mediun_setting = Entry(window, textvariable=lr_mediun, font=('Arial', 10))
        lr_mediun_setting.place(x=300, y=220)

        lr_small = StringVar()
        lr_small.set('-3,2')
        lr_small_setting = Entry(window, textvariable=lr_small, font=('Arial', 10))
        lr_small_setting.place(x=300, y=250)


        theta_large = StringVar()
        theta_large.set('15,20')
        theta_large_setting = Entry(window, textvariable=theta_large, font=('Arial', 10))
        theta_large_setting.place(x=300, y=280)

        theta_mediun = StringVar()
        theta_mediun.set('0,25')
        theta_mediun_setting = Entry(window, textvariable=theta_mediun, font=('Arial', 10))
        theta_mediun_setting.place(x=300, y=310)

        theta_small = StringVar()
        theta_small.set('-15,20')
        theta_small_setting = Entry(window, textvariable=theta_small, font=('Arial', 10))
        theta_small_setting.place(x=300, y=340)

        # tk.Label(window, text='', font=('Arial', 14)).place(x=700, y=450)
        self.btn_train = Button(window, text='train', command=lambda:train_model()).place(x=300, y=400)
        self.show = Button(window, text='show', command=lambda:get_map()).place(x=150, y=400)
        # self.messagebox = Message(window)
        # self.messagebox = ttk.showinfo(title=None, message=None)
        def train_model():
            para = Guassion_Function()
            para.f_large_mean = int(f_Large_setting.get().split(',')[0])
            para.f_large_dev = int(f_Large_setting.get().split(',')[1])
            para.f_medium_mean = int(f_medium_setting.get().split(',')[0])
            para.f_medium_dev = int(f_medium_setting.get().split(',')[1])
            para.f_small_mean = int(f_small_setting.get().split(',')[0])
            para.f_small_dev = int(f_small_setting.get().split(',')[1])
            para.lr_large_mean = int(lr_large_setting.get().split(',')[0])
            para.lr_large_dev = int(lr_large_setting.get().split(',')[1])
            para.lr_medium_mean = int(lr_mediun_setting.get().split(',')[0])
            para.lr_medium_dev = int(lr_mediun_setting.get().split(',')[1])
            para.lr_small_mean = int(lr_small_setting.get().split(',')[0])
            para.lr_small_dev = int(lr_small_setting.get().split(',')[1])

            para.theta_large_mean = int(theta_large_setting.get().split(',')[0])
            para.theta_large_dev = int(theta_large_setting.get().split(',')[1])
            para.theta_medium_mean = int(theta_mediun_setting.get().split(',')[0])
            para.theta_medium_dev = int(theta_mediun_setting.get().split(',')[1])
            para.theta_small_mean = int(theta_small_setting.get().split(',')[0])
            para.theta_small_dev = int(theta_small_setting.get().split(',')[1])

            select_file = self.comboExample.get()
            file = os.path.join(dir, select_file)
            way = self.comboway.current()
            print(way)

            is_success = main_run(para,file,way)
            if is_success:
                messagebox.showinfo(title='result', message='"success!!!! "')
            else:
                messagebox.showinfo(title='result', message='"碰！ Σヽ(ﾟД ﾟ; )ﾉ "')
            draw_moving_car(file)

        def get_map():
            select_file = self.comboExample.get()
            file = os.path.join(dir, select_file)
            draw_map(file)
            from PIL import Image
            # type+"_"+file+".png")
            file_name = str(self.comboExample.get()).replace('.txt', '.png')
            im = Image.open(file_name)
            print(im.size[0])
            print(im.size[1])
            nim = im.resize((70*5,65*5), Image.BILINEAR)
            nim.save(file_name)

            self.img = PhotoImage(file=file_name)
            self.org_canvas.itemconfig(self.imgArea, image=self.img)


#
# 第1步，例項化object，建立視窗window
window = Tk()
# 第2步，給視窗的視覺化起名字
window.title('My Window')
# 第3步，設定視窗的大小(長 * 寬)
window.geometry('900x500')  # 這裡的乘是小x
# 第4步，載入 wellcome image
file = [data for data in os.listdir(dir)]
app = skin()
window.mainloop()