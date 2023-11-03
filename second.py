import  cv2
import mediapipe as mp
import time
video=cv2.VideoCapture(0)

mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils
ptime=0
ctime=0
while True:
    s,frame=video.read()
    imgrgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)

    print(results.multi_hand_landmarks)
    if  results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                # print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id==0:
                    cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)
            mpdraw.draw_landmarks(frame,handlms,mphands.HAND_CONNECTIONS)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()