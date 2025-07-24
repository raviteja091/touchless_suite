import cv2, math
from common.hand_tracking import HandDetector
from directkeys import PressKey, ReleaseKey, a_pressed, d_pressed, w_pressed, s_pressed

det=HandDetector(maxHands=2)
cap=cv2.VideoCapture(0)
while True:
    ret,img=cap.read(); img=det.findHands(img)
    lm=det.findPosition(img,draw=False)
    if len(lm)>=6:
        x0,y0=lm[0][1:]
        x1,y1=lm[1][1:]
        dx,dy=x1-x0,y1-y0
        if dy>abs(dx)>50:
            ReleaseKey(a_pressed); ReleaseKey(d_pressed); PressKey(w_pressed)
        elif dx>dy>50:
            ReleaseKey(a_pressed); ReleaseKey(w_pressed); PressKey(d_pressed)
        elif -dx>dy>50:
            ReleaseKey(d_pressed); ReleaseKey(w_pressed); PressKey(a_pressed)
        else:
            ReleaseKey(a_pressed); ReleaseKey(d_pressed); PressKey(s_pressed)
    cv2.imshow("3DRace",img)
    if cv2.waitKey(1)==ord('q'):break
cap.release();cv2.destroyAllWindows()
