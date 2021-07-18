import cv2.cv2 as cv2
import os
import time
import HandTrackingModule as htm
from PIL import Image
#import pyttsx3 as p
#v2.namedWindow("first", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("first", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
wcam, hCam = 4000, 4000
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wcam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
folderPath = "FingerImages"
myList = os.listdir(folderPath)
#engine=p.init()
print(myList)
overLayList = []
for imgPath in myList:
    image = Image.open(f'{folderPath}/{imgPath}')
    image = image.resize((300, 300))
    image.save(f'{imgPath}')
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overLayList.append(image)


detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
findpoints = []
i,j,k=-1,-1,-1
flag=0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        fingers = []

        if lmlist[tipIds[0]][1] < lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFinger = fingers.count(1)
        flag=totalFinger
        # print(totalFinger)

        #h, w, c = overLayList[totalFinger - 1].shape
        #img[0:h, 0:w] = overLayList[totalFinger - 1]
        if totalFinger != 0 and lmlist[8][2] < lmlist[6][2] and i!=-1 and j!=-1 and k!=-1 and flag!=2 and flag!=5:
            findpoints.append([lmlist[8][1], lmlist[8][2]])
        for a, b in findpoints:
            if i!=-1 and j!=-1 and k!=-1 and flag!=2:
                cv2.circle(img, (a, b), 20, (i,j,k), cv2.FILLED)
        #if lmlist[8][2] < lmlist[6][2]:
            #engine.say("your indication finger is on")
            #cv2.putText(img,str("your indication finger is on"),(600,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),10)
           # engine.runAndWait()

        if lmlist[8][1]<=100 and lmlist[8][2]<=100:
            i,j,k=(0,255,0)
        if lmlist[8][1]<=200 and lmlist[8][2]<=100 and lmlist[8][1]>=100:
            i,j,k=(255,0,0)
        if lmlist[8][1]<=300 and lmlist[8][2]<=100 and lmlist[8][1]>=200:
            i,j,k=(0,0,255)
        if lmlist[8][1]<=400 and lmlist[8][2]<=100 and lmlist[8][1]>=300:
            i,j,k=(255,255,255)
        if lmlist[8][1]<=500 and lmlist[8][2]<=100 and lmlist[8][1]>=400:
            i,j,k=(0,0,0)
        if lmlist[8][1]<=600 and lmlist[8][2]<=100 and lmlist[8][1]>=500:
            i,j,k=(255,255,0)
    else:
        findpoints.clear()
    if flag==0:
            i,j,k=-1,-1,-1
            findpoints.clear()
    cv2.rectangle(img,(0,0),(100,100),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(100,0),(200,100),(255,0,0),cv2.FILLED)
    cv2.rectangle(img,(200,0),(300,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(img,(300,0),(400,100),(255,255,255),cv2.FILLED)
    cv2.rectangle(img,(400,0),(500,100),(0,0,0),cv2.FILLED)
    cv2.rectangle(img,(500,0),(600,100),(255,255,0),cv2.FILLED)
    cv2.imshow("first", img)
    cv2.waitKey(1)
