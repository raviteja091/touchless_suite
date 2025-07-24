import cv2, numpy as np, time, autopy
from common.hand_tracking import HandDetector

# Settings
WCam, HCam = 640, 480; frameR=100; smooth=7
cap=cv2.VideoCapture(0); cap.set(3,WCam); cap.set(4,HCam)
det=HandDetector(maxHands=1)
wScr,hScr=autopy.screen.size()
plocX,plocY=0,0

while True:
    ret,img = cap.read(); img=det.findHands(img)
    lm = det.findPosition(img, draw=False)
    if lm:
        x1,y1=lm[8][1:]
        fingers=det.fingersUp()
        cv2.rectangle(img, (frameR,frameR),(WCam-frameR,HCam-frameR),(255,0,255),2)
        # move
        if fingers[1]==1 and fingers[2]==0:
            x3 = np.interp(x1,(frameR,WCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,HCam-frameR),(0,hScr))
            clocX = plocX + (x3-plocX)/smooth
            clocY = plocY + (y3-plocY)/smooth
            autopy.mouse.move(wScr-clocX, clocY)
            plocX,plocY=clocX,clocY
        # click
        if fingers[1]==1 and fingers[2]==1:
            length,_ = det.findDistance(8,12,img)
            if length<40: autopy.mouse.click()
    cv2.imshow("Mouse",img)
    if cv2.waitKey(1)==ord('q'): break

cap.release(); cv2.destroyAllWindows()
