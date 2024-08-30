import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)
video = cv2.VideoCapture(0)

drawing=False
last_point=None
canvas=np.zeros((480,640,3),dtype=np.uint8)

def fingerDetectorLines(img,lmlist):
    if len(lmlist) >= 21:
        # Thumb
        cv2.line(img, (lmlist[0][0], lmlist[0][1]), (lmlist[1][0], lmlist[1][1]), (0, 255, 0), 2)  # Thumb segment 1
        cv2.line(img, (lmlist[1][0], lmlist[1][1]), (lmlist[2][0], lmlist[2][1]), (0, 255, 0), 2)  # Thumb segment 2
        cv2.line(img, (lmlist[2][0], lmlist[2][1]), (lmlist[3][0], lmlist[3][1]), (0, 255, 0), 2)  # Thumb segment 3
        cv2.line(img, (lmlist[3][0], lmlist[3][1]), (lmlist[4][0], lmlist[4][1]), (0, 255, 0), 2)  # Thumb segment 4
            
        # Index finger
        cv2.line(img, (lmlist[5][0], lmlist[5][1]), (lmlist[6][0], lmlist[6][1]), (0, 255, 0), 2)  # Index finger segment 1
        cv2.line(img, (lmlist[6][0], lmlist[6][1]), (lmlist[7][0], lmlist[7][1]), (0, 255, 0), 2)  # Index finger segment 2
        cv2.line(img, (lmlist[7][0], lmlist[7][1]), (lmlist[8][0], lmlist[8][1]), (0, 255, 0), 2)  # Index finger segment 3
            
        # Middle finger
        cv2.line(img, (lmlist[9][0], lmlist[9][1]), (lmlist[10][0], lmlist[10][1]), (0, 255, 0), 2)    # Middle finger segment 1
        cv2.line(img, (lmlist[10][0], lmlist[10][1]), (lmlist[11][0], lmlist[11][1]), (0, 255, 0), 2)  # Middle finger segment 2
        cv2.line(img, (lmlist[11][0], lmlist[11][1]), (lmlist[12][0], lmlist[12][1]), (0, 255, 0), 2)  # Middle finger segment 3
            
        # Ring finger
        cv2.line(img, (lmlist[13][0], lmlist[13][1]), (lmlist[14][0], lmlist[14][1]), (0, 255, 0), 2)  # Ring finger segment 1
        cv2.line(img, (lmlist[14][0], lmlist[14][1]), (lmlist[15][0], lmlist[15][1]), (0, 255, 0), 2)  # Ring finger segment 2
        cv2.line(img, (lmlist[15][0], lmlist[15][1]), (lmlist[16][0], lmlist[16][1]), (0, 255, 0), 2)  # Ring finger segment 3
            
        # Pinky finger
        cv2.line(img, (lmlist[17][0], lmlist[17][1]), (lmlist[18][0], lmlist[18][1]), (0, 255, 0), 2)  # Pinky finger segment 1
        cv2.line(img, (lmlist[18][0], lmlist[18][1]), (lmlist[19][0], lmlist[19][1]), (0, 255, 0), 2)  # Pinky finger segment 2
        cv2.line(img, (lmlist[19][0], lmlist[19][1]), (lmlist[20][0], lmlist[20][1]), (0, 255, 0), 2)  # Pinky finger segment 3
        cv2.line(img, (lmlist[0][0], lmlist[0][1]), (lmlist[17][0], lmlist[17][1]), (0, 255, 0), 2)    # Pinky finger segment 4
            
        # Palm connections
        cv2.line(img, (lmlist[5][0], lmlist[5][1]), (lmlist[9][0], lmlist[9][1]), (0, 255, 0), 2)      # Index to middle base
        cv2.line(img, (lmlist[9][0], lmlist[9][1]), (lmlist[13][0], lmlist[13][1]), (0, 255, 0), 2)    # Middle to ring base
        cv2.line(img, (lmlist[13][0], lmlist[13][1]), (lmlist[17][0], lmlist[17][1]), (0, 255, 0), 2)  # Ring to pinky base


    for lm in lmlist:
        cv2.circle(img, (lm[0], lm[1]), 5, (255, 0, 0), cv2.FILLED)

def drawLines(img, lmlist):
    global last_point, drawing
    if len(lmlist) >= 21:
        indexTip = (lmlist[8][0], lmlist[8][1])
        if detector.fingersUp(hand) == [0, 1, 0, 0, 0]:  
            
            if drawing:
                if last_point:
                    cv2.line(canvas, last_point, indexTip, (0, 0, 255), 5)
                last_point = indexTip
            else:
                drawing = True
                last_point = indexTip
        elif detector.fingersUp(hand)==[0,0,0,0,0]:
            cv2.circle(canvas,indexTip,50,(0,0,0),-1)
            # last_point=None
            drawing=False
        else:
            drawing = False
            last_point = None
    
    img = cv2.addWeighted(img, 1, canvas, 0.5, 0)
    return img

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)  
    if hands:
        hand = hands[0] 
        lmlist = hand['lmList'] 

        fingerDetectorLines(img,lmlist)
        img=drawLines(img,lmlist)

        if lmlist:
            fingerUp = detector.fingersUp(hand)
            if fingerUp == [0, 1, 0, 0, 0]:
                print("1 finger up")
            elif fingerUp == [0, 1, 1, 0, 0]:
                print("2 fingers up")
            elif fingerUp == [0, 1, 1, 1, 0]:
                print("3 fingers up")
            elif fingerUp == [0, 1, 1, 1, 1]:
                print("4 fingers up")
            elif fingerUp == [1, 1, 1, 1, 1]:
                print("All fingers are up") 
            elif fingerUp == [0,0,0,0,0]:
                print("Fingers are wrapped") 
    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()