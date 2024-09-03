import cv2
from HandTracker import HandTracker

video = cv2.VideoCapture(0)
tracker = HandTracker(maxHands=1, detectionCon=0.8)

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = tracker.findHands(img)
    
    tracker.drawColorButtons(img)

    if hands:
        hand = hands[0]
        lmlist = hand['lmList']
        tracker.fingerDetectorLines(img, lmlist)
        img = tracker.drawLines(img, lmlist, hand)

        fingerUp = tracker.detector.fingersUp(hand)
        if fingerUp == [0, 1, 1, 0, 0]:
            indexTip = lmlist[8][0], lmlist[8][1]
            tracker.checkColorChange(indexTip[0], indexTip[1])
            print("1 finger up")
        elif fingerUp == [0, 1, 1, 0, 0]:
            print("2 fingers up")
        elif fingerUp == [0, 1, 1, 1, 0]:
            print("3 fingers up")
        elif fingerUp == [0, 1, 1, 1, 1]:
            print("4 fingers up")
        elif fingerUp == [1, 1, 1, 1, 1]:
            print("All fingers are up")
        elif fingerUp == [0, 0, 0, 0, 0]:
            print("Fingers are wrapped")

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
