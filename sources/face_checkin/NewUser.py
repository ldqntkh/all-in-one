import cv2
import sqlite3

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Hàm cập nhật tên và ID vào CSDL
def insertOrUpdate(id, name):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute('SELECT * FROM People WHERE ID='+str(id))
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist==1:
        cmd="UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(id)
    else:
        cmd="INSERT INTO people(ID,Name) Values("+str(id)+",' "+str(name)+" ' )"

    conn.execute(cmd)
    conn.commit()
    conn.close()
    
def findUser(id):
    conn=sqlite3.connect("../database/db.sqlite3")
    cursor=conn.execute('SELECT id FROM auth_user WHERE username="'+ id + '"')
    user = None
    for row in cursor:
        user = row
        break
    conn.close()
    return user

findUserInformation = True
while( findUserInformation ):
    id=input('Nhập UserName nhân viên:')
    find = findUser(id)
    if find != None:
        id = find[0]
        findUserInformation = False

print("Bắt đầu chụp ảnh nhân viên, nhấn q để thoát!")

# insertOrUpdate(id)

sampleNum=0
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)
fx = fy = fx1 = fy1 = None



while(True):

    ret, img = cam.read()
    
    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img,1)
    
    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
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
    
    # Đưa ảnh về ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # check face có nằm trong vùng cho phép không
        if x < fx or x + w > fx1: 
            continue
        if y < fy or y + h > fy1: 
            continue
        
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        sampleNum = sampleNum + 1
        # Ghi vòng lặp đang thực hiện ra khung hình
        cv2.putText(img, "Process: " + str(sampleNum) + "%", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)
        # Ghi dữ liệu khuôn mặt vào thư mục dataSet
        cv2.imwrite("dataSet/User." + str(id) + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('frame', img)
    # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif sampleNum>=100:
        break

cam.release()
cv2.destroyAllWindows()
