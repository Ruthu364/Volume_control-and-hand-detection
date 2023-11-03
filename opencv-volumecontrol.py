
import  cv2
import mediapipe as mp
import time
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vr=volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-10.0, None)
mv=vr[0]
maxv=vr[1]


video=cv2.VideoCapture(0)

mphands=mp.solutions.hands
hands=mphands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpdraw=mp.solutions.drawing_utils
ptime=0
ctime=0
while True:
    s,frame=video.read()
    imgrgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)

    # print(results.multi_hand_landmarks)
    if  results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                # print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if(id==4):
                    x1=cx
                    y1=cy
                if(id==8):
                    x2=cx
                    y2=cy   
                # print(id,cx,cy)
                if (id==4 or id==8):
                    cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)    
            mpdraw.draw_landmarks(frame,handlms,mphands.HAND_CONNECTIONS)
            cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)
            cv2.circle(frame,((x2+x1)//2,(y2+y1)//2),15,(255,0,255),cv2.FILLED)
            length=math.hypot(x2-x1,y2-y1)
            # print(length)
            v=np.interp(length,[20,180],[mv,maxv])
            # print(v)
            volume.SetMasterVolumeLevel(v, None)
            if(length<30):
                 cv2.circle(frame,((x2+x1)//2,(y2+y1)//2),15,(0,255,0),cv2.FILLED)    

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(frame,f'FPS:{int(fps)}',(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()