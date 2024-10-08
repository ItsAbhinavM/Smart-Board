import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from datetime import datetime

class HandTracker:
    def __init__(self, maxHands=1, detectionCon=0.8):
        self.detector = HandDetector(maxHands=maxHands, detectionCon=detectionCon)
        self.canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        self.drawing = False
        self.last_point = None
        self.current_color = (0, 0, 255)  
        self.current_thickness=5
        self.thumbs_up_saved = False

        self.color_buttons = [
            {"color": (0, 0, 255), "pos": (90, 0, 85,75)},
            {"color": (0, 255, 0), "pos": (180, 0, 85,75)},
            {"color": (255, 0, 0), "pos": (270, 0, 85,75)},  
            {"color": (0, 255, 255), "pos": (350, 0, 85,75)},
        ]

        self.thickness_boxes = [
            {"pos": (570, 100, 65, 65), "text": 'pen'},
            {"pos": (570, 170, 65, 65), "text": 1},  
            {"pos": (570, 240, 65, 65), "text": 2},
            {"pos": (570, 310, 65, 65), "text": 3}
        ]

    def fingerDetectorLines(self, img, lmlist):
        if len(lmlist) >= 21:
            # Thumb
            cv2.line(img, (lmlist[0][0], lmlist[0][1]), (lmlist[1][0], lmlist[1][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[1][0], lmlist[1][1]), (lmlist[2][0], lmlist[2][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[2][0], lmlist[2][1]), (lmlist[3][0], lmlist[3][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[3][0], lmlist[3][1]), (lmlist[4][0], lmlist[4][1]), (0, 255, 0), 2)
                
            # Index finger
            cv2.line(img, (lmlist[5][0], lmlist[5][1]), (lmlist[6][0], lmlist[6][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[6][0], lmlist[6][1]), (lmlist[7][0], lmlist[7][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[7][0], lmlist[7][1]), (lmlist[8][0], lmlist[8][1]), (0, 255, 0), 2)
                
            # Middle finger
            cv2.line(img, (lmlist[9][0], lmlist[9][1]), (lmlist[10][0], lmlist[10][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[10][0], lmlist[10][1]), (lmlist[11][0], lmlist[11][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[11][0], lmlist[11][1]), (lmlist[12][0], lmlist[12][1]), (0, 255, 0), 2)
                
            # Ring finger
            cv2.line(img, (lmlist[13][0], lmlist[13][1]), (lmlist[14][0], lmlist[14][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[14][0], lmlist[14][1]), (lmlist[15][0], lmlist[15][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[15][0], lmlist[15][1]), (lmlist[16][0], lmlist[16][1]), (0, 255, 0), 2)
                
            # Pinky finger
            cv2.line(img, (lmlist[17][0], lmlist[17][1]), (lmlist[18][0], lmlist[18][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[18][0], lmlist[18][1]), (lmlist[19][0], lmlist[19][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[19][0], lmlist[19][1]), (lmlist[20][0], lmlist[20][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[0][0], lmlist[0][1]), (lmlist[17][0], lmlist[17][1]), (0, 255, 0), 2)
                
            # Palm connections
            cv2.line(img, (lmlist[5][0], lmlist[5][1]), (lmlist[9][0], lmlist[9][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[9][0], lmlist[9][1]), (lmlist[13][0], lmlist[13][1]), (0, 255, 0), 2)
            cv2.line(img, (lmlist[13][0], lmlist[13][1]), (lmlist[17][0], lmlist[17][1]), (0, 255, 0), 2)

        for lm in lmlist:
            cv2.circle(img, (lm[0], lm[1]), 5, (255, 0, 0), cv2.FILLED)

    def drawColorButtons(self, img):
        for button in self.color_buttons:
            x, y, w, h = button["pos"]
            color=button['color']
            if color==self.current_color:
                cv2.rectangle(img,(x-5, y-5), (x + w+5, y + h+5),(255,255,255),cv2.FILLED)
            cv2.rectangle(img, (x, y), (x + w, y + h), button["color"], cv2.FILLED)
        cv2.rectangle(img, (450, 0), (450 + 90, 0 + 75), (255,255,255))
        cv2.putText(img, 'Colors',(455, 45),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    def drawThicknessButtons(self,img):
        for button in self.thickness_boxes:
            x, y, w, h = button["pos"]
            thickness=button['text']
            if thickness=='pen':
                cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255))
                cv2.putText(img,str(thickness),(x+10,y+37),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255),2)
            else :
                if thickness * 5 == self.current_thickness:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (255, 255, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,0),cv2.FILLED)
                cv2.putText(img,str(thickness),(x+25,y+37),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255),2)

    def checkColorChange(self, x, y):
        for button in self.color_buttons:
            bx, by, bw, bh = button["pos"]
            if bx < x < bx + bw and by < y < by + bh:
                self.current_color = button["color"]
    
    def checkThichknessChange(self,x,y):
        for button in self.thickness_boxes:
            bx, by, bw, bh = button["pos"]
            if bx < x < bx + bw and by < y < by + bh:
                if isinstance(button['text'],int):
                    self.current_thickness=button['text']*5
                    print(f"thickness changed to {self.current_thickness}")

    def drawLines(self, img, lmlist, hand):
        if len(lmlist) >= 21:
            indexTip = (lmlist[8][0], lmlist[8][1])
            if self.detector.fingersUp(hand) == [0, 1, 0, 0, 0]:
                if self.drawing:
                    if self.last_point:
                        global current_thickness
                        cv2.line(self.canvas, self.last_point, indexTip, self.current_color, self.current_thickness)
                    self.last_point = indexTip
                else:
                    self.drawing = True
                    self.last_point = indexTip
            elif self.detector.fingersUp(hand) == [0, 0, 0, 0, 0]:
                cv2.circle(self.canvas, indexTip, 50, (0, 0, 0), -1)
                self.drawing = False
            else:
                self.drawing = False
                self.last_point = None
        
        img = cv2.addWeighted(img, 1, self.canvas, 0.5, 0)
        return img
    
    def saveCanvas(self):
        now=datetime.now()
        formattedTime = now.strftime("%d-%m-%Y_%H-%M")
        file_name = f"Saved_Boards/canvas_{formattedTime}.png"
        cv2.imwrite(file_name, self.canvas)
        print("image saved")
        
    def findHands(self, img):
        hands, img = self.detector.findHands(img, draw=False)
        return hands, img