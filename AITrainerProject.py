import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("AiTrainer/curls.mp4")
detector = pm.PoseDetector()
count = 0
dir = 0
ptime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img,(1280, 720))
    #img = cv2.imread("AiTrainer/test.jpg")
    #img = cv2.resize(img, (720, 720))
    img = detector.draw_landmarks(img,draw=False)
    landmarks_list = detector.find_landmarks(img, draw=False)
    #print(landmarks_list)
    if len(landmarks_list)!=0:
        #Left arm
        #img = detector.find_angle(img,11,13,15)
        #Right arm
        angle = detector.find_angle(img,12,14,16)
        per = np. interp(angle,(35,135),(100,0))
        bar = np.interp(angle,(35,135),(100,650))
        #print(angle,per)

        #Check the dumbbell curls
        color = (255,0,255)
        if per == 100:
            color = (0,255,0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0,255,0)
            if dir == 1:
                count += 0.5
                dir =0
        print(count)
        #Draw Bar
        cv2.rectangle(img,(1100,100),(1175,650),color,3)
        cv2.rectangle(img,(1100,int(bar)),(1175,650),color,cv2.FILLED)
        cv2.putText(img,f'{int(per)}%',(1100,75),cv2.FONT_HERSHEY_PLAIN,4,color,4)

        #Draw curl count
        cv2.rectangle(img, (0,450),(250,720),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(count)}',(45,670),cv2.FONT_HERSHEY_PLAIN,15,(255,0,0),25)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img,f'{int(fps)}',(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)