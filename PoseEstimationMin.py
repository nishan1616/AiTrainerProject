import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture('PoseVideos/1.mp4')
ptime = 0
ctime = 0

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)
    #print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    for id, landmark in enumerate(results.pose_landmarks.landmark):
        h,w,c = img.shape
        print(id, landmark)
        cx,cy = int(landmark.x*w), int(landmark.y*h)
        cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)