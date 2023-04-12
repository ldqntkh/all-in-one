from tkinter import *
import cv2
from PIL import Image, ImageTk

from helper.dbHelperFunctions import DBHelperFunctions



class TimeKeeping:
    def __init__(self, parent):
        self.startingCamera = False
        self.imgtk = None
        self.panelForm = PanedWindow(parent.panelForm)
        self.panelForm.pack()
        self.imgtk = Label(self.panelForm)
        self.imgtk.pack()
        
        self.findedUser = False
        
        # Khởi tạo bộ phát hiện khuôn mặt
        self.faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cam=cv2.VideoCapture(0)
        # Khởi tạo bộ nhận diện khuôn mặt
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('recognizer/trainner.yml')
        
        self.startCamera()
           
    def startCamera(self):
        if self.startingCamera == True:
            return None
        
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 1
        fontcolor = (0,255,0)
        fontcolor1 = (0,0,255)  
        fx = fy = fx1 = fy1 = None
        sizeboxW = 300
        sizeboxH = 400
        # Đọc ảnh từ camera
        ret,img = self.cam.read()

        # Lật ảnh cho đỡ bị ngược
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        # img = cv2.resize(img, (monitor.width, monitor.height))  
        # img = cv2.resize(img, (sizeboxW, sizeboxH))  
        x = img.shape[1]/2 - sizeboxW/2
        y = img.shape[0]/2 - sizeboxH/2
        
        img = img[int(y):int(y+sizeboxH), int(x):int(x+sizeboxW)]

        # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
        # centerH = img.shape[0] // 2
        # centerW = img.shape[1] // 2
        
        # cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
        #             (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

        # fx = centerW - sizeboxW // 2
        # fy = centerH - sizeboxH // 2
        # fx1 = centerW + sizeboxW // 2
        # fy1 = centerH + sizeboxH // 2
        percent = 25
        cv2.rectangle(img, (percent, percent),
                    (sizeboxW - percent, sizeboxH - percent), (255, 255, 255), 5)
        fx = percent
        fy = percent
        fx1 = sizeboxW - percent
        fy1 = sizeboxH - percent
        
        # Chuyển ảnh về xám
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Phát hiện các khuôn mặt trong ảnh camera
        faces = self.faceDetect.detectMultiScale(gray,1.3,5)

        # Lặp qua các khuôn mặt nhận được để hiện thông tin
        for(x,y,w,h) in faces:
            if x < fx or x + w > fx1: 
                continue
            if y < fy or y + h > fy1: 
                continue
            # Vẽ hình chữ nhật quanh mặt
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (dộ sai khác)
            id,dist = self.recognizer.predict(gray[y:y+h,x:x+w])

            profile=None
            # Nếu độ sai khác
            if int(dist) < 70 and id:
                profile = self.getProfile(id)
            # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
            if profile is not None:
                self.findedUser = True
                # cv2.putText(img, "Name: " + str(profile[4]) + " " + str(profile[5]), (fx, fy1 + 30), fontface, fontscale, fontcolor ,2)
                cv2.putText(img, "Name: " + str(profile[4]) + " " + str(profile[5]), (x, y + h + 30), fontface, fontscale, fontcolor ,2)
            else:
                cv2.putText(img, "Name: Unknown", (fx, fy1 + 30), fontface, fontscale, fontcolor1, 2)


        # cv2.imshow('Face',img)
        img = img[:,:,::-1]
        im = Image.fromarray(img)
        img2 = ImageTk.PhotoImage(image=im) 
        
        # img2 = ImageTk.PhotoImage(img)
        self.imgtk.configure(image=img2)
        self.imgtk.image = img2
        
        # Nếu nhấn q thì thoát
        # if cv2.waitKey(1)==ord('q'):
        #     break
      
        if self.findedUser == True:
            self.cam.release()
            cv2.destroyAllWindows()
        else :
            self.panelForm.after(5, self.startCamera)
            
    def getProfile(self, id):
        db = DBHelperFunctions()
        profile = db.getUserById(id)
        return profile