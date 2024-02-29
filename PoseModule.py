import cv2
import mediapipe as mp
import time
import math

class PoseDetector():
    def __init__(self, mode=False, smooth=True, detection_con=0.5, tracking_con=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=self.mode, smooth_landmarks=self.smooth,
                                      min_detection_confidence=self.detection_con,
                                      min_tracking_confidence=self.tracking_con)
        self.mp_draw = mp.solutions.drawing_utils

    def draw_landmarks(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def find_landmarks(self, img, draw=True):
        self.landmark_list = []
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, landmark)
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                self.landmark_list.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmark_list

    def find_angle(self,img,p1,p2,p3,draw=True):
        x1,y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        x3, y3 = self.landmark_list[p3][1:]
        #Calculate the angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle<0:
            angle += 360
        #print(angle)
        #Draw
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
            cv2.line(img,(x3,y3),(x2,y2),(255,255,0),3)
            cv2.circle(img,(x1,y1),10,(0,0,255),cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img,(x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img,(x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            #cv2.putText(img,str(int(angle)),(x2-50,y2+50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return angle
def main():
    cap = cv2.VideoCapture('PoseVideos/1.mp4')
    ptime = 0
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        img = detector.draw_landmarks(img)
        landmark_list = detector.find_landmarks(img, draw = False)
        if len(landmark_list) != 0:
            print(landmark_list[14])
            cv2.circle(img, (landmark_list[14][1], landmark_list[14][2]), 15, (0, 0, 255), cv2.FILLED)
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
