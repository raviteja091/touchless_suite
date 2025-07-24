import cv2, time
from common.hand_tracking import HandDetector
from directkeys import PressKey, ReleaseKey, left_pressed, right_pressed

det=HandDetector(maxHands=1)
cap=cv2.VideoCapture(0)
state=None
while True:
    ret,img=cap.read(); img=det.findHands(img)
    fingers=det.fingersUp()
    total=fingers.count(1)
    if total==0 and state!='brake':
        ReleaseKey(right_pressed); PressKey(left_pressed); state='brake'
    if total==5 and state!='gas':
        ReleaseKey(left_pressed); PressKey(right_pressed); state='gas'
    if total not in (0,5) and state:
        ReleaseKey(left_pressed); ReleaseKey(right_pressed); state=None
    cv2.imshow("Hill",img)
    if cv2.waitKey(1)==ord('q'):break
cap.release();cv2.destroyAllWindows()
