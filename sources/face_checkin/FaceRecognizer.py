import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

# Khởi tạo bộ phát hiện khuôn mặt
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Khởi tạo bộ nhận diện khuôn mặt
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainner.yml')



id=0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)
fx = fy = fx1 = fy1 = None
# Hàm lấy thông tin người dùng qua ID
def getProfile(id):
    conn=sqlite3.connect("../database/db.sqlite3")
    cursor=conn.execute("SELECT * FROM auth_user WHERE id="+str(id))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

# Khởi tạo camera
cam=cv2.VideoCapture(0)

while(True):

    # Đọc ảnh từ camera
    ret,img=cam.read()

    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img, 1)

    # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
    centerH = img.shape[0] // 2
    centerW = img.shape[1] // 2
    sizeboxW = 600
    sizeboxH = 700
    cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

    fx = centerW - sizeboxW // 2
    fy = centerH - sizeboxH // 2
    fx1 = centerW + sizeboxW // 2
    fy1 = centerH + sizeboxH // 2
    # Chuyển ảnh về xám
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Phát hiện các khuôn mặt trong ảnh camera
    faces=faceDetect.detectMultiScale(gray,1.3,5)

    # Lặp qua các khuôn mặt nhận được để hiện thông tin
    for(x,y,w,h) in faces:
        if x < fx or x + w > fx1: 
            continue
        if y < fy or y + h > fy1: 
            continue
        # Vẽ hình chữ nhật quanh mặt
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (dộ sai khác)
        id,dist=recognizer.predict(gray[y:y+h,x:x+w])

        profile=None

        # Nếu độ sai khác < 25% thì lấy profile
        if (dist<=20):
            profile=getProfile(id)

        # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
        if(profile!=None):
            cv2.putText(img, "Name: " + str(profile[4]) + " " + str(profile[5]), (fx, fy1 + 30), fontface, fontscale, fontcolor ,2)
        else:
            cv2.putText(img, "Name: Unknown", (fx, fy1 + 30), fontface, fontscale, fontcolor1, 2)


    cv2.imshow('Face',img)
    # Nếu nhấn q thì thoát
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

