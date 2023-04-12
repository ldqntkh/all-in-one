from tkinter import *

from components.registerNewUser import RegisterUser
from components.timeKeeping import TimeKeeping

class MainLayout:
    def __init__(self, window):
        self.window = window
        self.panelForm = None
        self.page = 'main'
        
        self.showLayout()
        
        
    def showLayout(self):
        if self.panelForm:
            self.panelForm.destroy()
        
        self.panelForm = PanedWindow(self.window)
        self.panelForm.pack()
        
        match self.page:
            case "main":
                Button(self.panelForm, text="Đăng ký thành viên", command=self.showRegisterPage, width=10, padx=10).grid(row=1, column=3, padx=10, pady=10)
                Button(self.panelForm, text="Chấm công", command=self.showTimekeeping, width=10, padx=10).grid(row=2, column=3, padx=10, pady=10)
                Button(self.panelForm, text="Quit", command=self.window.destroy, width=10, padx=10).grid(row=5, column=3, padx=10, pady=10)
            case 'register':
                RegisterUser(self)
            case 'timekeeping':
                TimeKeeping(self)
        
    # show register page
    def showRegisterPage(self):
        self.page = 'register'
        self.window.after(0, self.showLayout)
    
    # show Timekeeping page
    def showTimekeeping(self):
        self.page = 'timekeeping'
        self.window.after(0, self.showLayout)
    
    #  goback main page
    def goBack(self):
        self.page = 'main'
        self.window.after(0, self.showLayout)