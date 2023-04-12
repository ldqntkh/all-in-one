

import cv2
# from screeninfo import get_monitors

class DetectNewFace:
    
    def __init__(self):
        self.sampleNum=0
        self.cam = cv2.VideoCapture(0)
        self.detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    def detect(self, id ):
        if self.sampleNum >= 100:
            return None 
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 1
        fontcolor1 = (0,0,255)
        fx = fy = fx1 = fy1 = None
        sizeboxW = 300
        sizeboxH = 400
        
        # monitor = get_monitors()[0]
        # sWidth = (monitor.width - sizeboxW - 50) // 2
        # sHeight = (monitor.height - sizeboxH - 50) // 2
        # cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        ret, img = self.cam.read()
        
        # Lật ảnh cho đỡ bị ngược
        img = cv2.flip(img,1)
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        # img = cv2.resize(img, (monitor.width, monitor.height))  
        # img = cv2.resize(img, (sizeboxW, sizeboxH))  
        x = img.shape[1]/2 - sizeboxW/2
        y = img.shape[0]/2 - sizeboxH/2
        
        img = img[int(y):int(y+sizeboxH), int(x):int(x+sizeboxW)]
        # img = cv2.resize(img, (w, h)) 
        
        # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
        # centerH = int(img.shape[0] // 1.5)
        # centerW = int(img.shape[1] // 1.5)
        percent = 25
        cv2.rectangle(img, (percent, percent),
                    (sizeboxW - percent, sizeboxH - percent), (255, 255, 255), 5)
        fx = percent
        fy = percent
        fx1 = sizeboxW - percent
        fy1 = sizeboxH - percent
        
        # Đưa ảnh về ảnh xám
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Nhận diện khuôn mặt
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # check face có nằm trong vùng cho phép không
            if x < fx or x + w > fx1: 
                continue
            if y < fy or y + h > fy1: 
                continue
            self.sampleNum = self.sampleNum + 1
            # Vẽ hình chữ nhật quanh mặt nhận được
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Ghi vòng lặp đang thực hiện ra khung hình
            cv2.putText(img, "Process: " + str(self.sampleNum) + "%", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)
            # Ghi dữ liệu khuôn mặt vào thư mục dataSet
            cv2.imwrite("dataSet/User." + str(id) + '.' + str(self.sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            
        
        # cv2.imshow('Face', img)
        return img
        
    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()