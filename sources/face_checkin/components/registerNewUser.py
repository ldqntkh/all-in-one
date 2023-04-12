from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

from helper.dbHelperFunctions import DBHelperFunctions
from lib.detectNewFace import DetectNewFace
from lib.trainModel import TrainModel


class RegisterUser:
    def __init__(self, parent):
        self.parent = parent
        self.init = 1
        self.processLabel = 0
        self.stringProcess = StringVar(value="")
        self.panelForm = PanedWindow(parent.panelForm)
        self.panelForm.pack()
        
        self.imgtk = Label(self.panelForm)
        self.imgtk.grid(row=7, columnspan=2)
        
        self.detectFace = DetectNewFace()
        self.userId = None
        
        self.showLayout()
        
    def showLayout(self):
        Label(self.panelForm, text="Mã nhân viên").grid(row=2, column=0,ipadx=10)
        username = Entry(self.panelForm, font=("Helvetica", 16))
        username.grid(row=2, column=1, ipadx=10)
        
        Label(self.panelForm, textvariable=self.stringProcess).grid(row=3, columnspan=2,padx=10, pady=10)
        
        Button(self.panelForm, text="Đăng ký gương mặt", command=lambda: self.registerFace(username.get())).grid(row=4, columnspan=2, padx=10, pady=10)
        Button(self.panelForm, text="Thoát", command=self.parent.goBack).grid(row=5, columnspan=2, padx=10, pady=10)
        
    def registerFace(self, username):
        db = DBHelperFunctions()
        user = db.getUserByUserName(username)
        if user is None:
           messagebox.showwarning("Thông báo", "Tên người dùng này chưa được đăng ký.")
           return False
        # hiển thị camera lấy gương mặt
        self.userId = user[0]
        self.showCamera()
        
    def showCamera(self):
        results = self.detectFace.detect(self.userId)
        if results is not None and self.detectFace.sampleNum <= 100:
            results = results[:,:,::-1]
            im = Image.fromarray(results)
            
            img2 = ImageTk.PhotoImage(image=im) 
            
            self.imgtk.configure(image=img2)
            self.imgtk.image = img2
            
            self.panelForm.after(5, self.showCamera)
        else :
            self.imgtk.grid_remove()
            self.detectFace.release()
            self.afterDetectUser()
        
    def afterDetectUser(self):
        # messagebox.showwarning("Thông báo", "Đã đăng ký gương mặt thành công")
        # train model
        TrainModel().train(self.stringProcess, self.success)
        
    def success(self):
        messagebox.showwarning("Thông báo", "Đã đăng ký gương mặt thành công")