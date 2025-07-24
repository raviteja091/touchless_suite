import cv2, time
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey, space_pressed

det=HandDetector(detectionCon=0.8, maxHands=1)
pressed=False
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    hands,img=det.findHands(frame); fingers=det.fingersUp(hands[0]) if hands else []
    if fingers==[0,0,0,0,0] and not pressed:
        PressKey(space_pressed); pressed=True
    if fingers!=[0,0,0,0,0] and pressed:
        ReleaseKey(space_pressed); pressed=False
    cv2.imshow("Dino",img)
    if cv2.waitKey(1)==ord('q'):break
cap.release();cv2.destroyAllWindows()
