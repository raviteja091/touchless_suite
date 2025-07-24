import cv2, math, numpy as np, pyautogui, autopy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from common.hand_tracking import HandDetector

# init
det=HandDetector(maxHands=1, detectionCon=0.85)
cap=cv2.VideoCapture(0); cap.set(3,640); cap.set(4,480)
# audio
dev=AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
vol=cast(dev, POINTER(IAudioEndpointVolume))
minV, maxV, _ = vol.GetVolumeRange()  # e.g. -63.5,0.0,0.5

mode='N'; active=False
while True:
    ret,img=cap.read(); img=det.findHands(img)
    lm=det.findPosition(img,draw=False); fingers=det.fingersUp()
    # select mode
    if not active:
        if fingers in ([0,1,0,0,0],[0,1,1,0,0]):
            mode='Scroll'; active=True
        elif fingers==[1,1,0,0,0]:
            mode='Volume'; active=True
        elif fingers==[1,1,1,1,1]:
            mode='Cursor'; active=True
    # Scroll
    if mode=='Scroll':
        if fingers==[0,1,0,0,0]: pyautogui.scroll(300)
        if fingers==[0,1,1,0,0]: pyautogui.scroll(-300)
        if fingers==[0,0,0,0,0]: active=False; mode='N'
    # Volume
    if mode=='Volume' and lm:
        x1,y1=lm[4][1:], lm[8][1:]
        length=math.hypot(x1[0]-y1[0], x1[1]-y1[1])
        level=np.interp(length,[50,200],[minV,maxV])
        vol.SetMasterVolumeLevel(level,None)
        if fingers[-1]==1: active=False; mode='N'
    # Cursor
    if mode=='Cursor' and lm:
        x,y=lm[8][1:]
        w,h=autopy.screen.size()
        X=np.interp(x,[110,620],[0,w]); Y=np.interp(y,[20,350],[0,h])
        autopy.mouse.move(X,Y)
        if fingers[0]==0: pyautogui.click()
        if fingers[1:]==[0,0,0,0]: active=False; mode='N'

    cv2.imshow("Ctrl",img)
    if cv2.waitKey(1)==ord('q'): break

cap.release(); cv2.destroyAllWindows()
