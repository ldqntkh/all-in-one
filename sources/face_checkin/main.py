from tkinter import *


from components.mainLayout import MainLayout
window_width = 500
window_height = 800
def center(toplevel):
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    toplevel.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))  
    
#Create an instance of tkinter frame
win = Tk()
# win.attributes('-fullscreen', True)
win.title("Hệ thống chấm công")
center(win)

MainLayout(win)

win.mainloop()