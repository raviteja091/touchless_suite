import os, cv2, numpy as np
from common.hand_tracking import HandDetector

# Settings
WIDTH, HEIGHT = 1280, 720
GESTURE_LINE = 300
DEBOUNCE = 30

# Initialize
slides = sorted(os.listdir("touchless_suite/presentation/slides"), key=len)
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH); cap.set(4, HEIGHT)
detector = HandDetector(detectionCon=0.8, maxHands=1)

imgIdx = 0; btnPressed=False; counter=0
annotations=[[]]; annIdx=-1; annStart=False

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    slide = cv2.imread(f"touchless_suite/presentation/slides/{slides[imgIdx]}")
    frame = detector.findHands(frame)
    lm = detector.findPosition(frame, draw=False)
    fingers = detector.fingersUp()

    # gesture line
    cv2.line(frame,(0,GESTURE_LINE),(WIDTH,GESTURE_LINE),(0,255,0),5)

    if lm and not btnPressed:
        cx, cy = lm[8][1], lm[8][2]
        # next/prev slides
        if cy < GESTURE_LINE:
            if fingers==[1,0,0,0,0] and imgIdx>0:
                imgIdx-=1; annotations=[[]]; annIdx=-1; annStart=False; btnPressed=True
            if fingers==[0,0,0,0,1] and imgIdx < len(slides)-1:
                imgIdx+=1; annotations=[[]]; annIdx=-1; annStart=False; btnPressed=True
        # draw
        if fingers==[0,1,0,0,0]:
            if not annStart:
                annStart=True; annIdx+=1; annotations.append([])
            annotations[annIdx].append((cx,cy))
            cv2.circle(slide,(cx,cy),5,(0,0,255),cv2.FILLED)
        else:
            annStart=False
    # debounce
    if btnPressed:
        counter +=1
        if counter>DEBOUNCE: btnPressed=False; counter=0

    # render annotations
    for stroke in annotations:
        for i in range(1,len(stroke)):
            cv2.line(slide, stroke[i-1], stroke[i], (0,0,200), 5)

    cv2.imshow("Slide", slide)
    if cv2.waitKey(1)==ord('q'): break

cap.release(); cv2.destroyAllWindows()
