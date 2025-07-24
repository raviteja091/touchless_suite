import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(mode, maxHands, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw:
            for lm in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, lm, self.hands_module.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            h,w,c = img.shape
            for id, lm in enumerate(myHand.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append((id, cx, cy))
                if draw: cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
        return lmList

    def fingersUp(self):
        fingers = []
        if not hasattr(self, 'results'): return [0,0,0,0,0]
        lm = {id:(x,y) for id,x,y in self.lmList}
        # Thumb
        fingers.append(1 if lm[4][0] > lm[3][0] else 0)
        # Other fingers
        for id in range(1,5):
            fingers.append(1 if lm[self.tipIds[id]][1] < lm[self.tipIds[id]-2][1] else 0)
        return fingers

    def findDistance(self, p1,p2,img,draw=True):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.circle(img,(x1,y1),5,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),5,(0,255,0),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        return length, img
