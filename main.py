import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)
video = cv2.VideoCapture(0)

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)

    if hands:
        hand = hands[0]
        lmlist = hand['lmList']
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

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
print("hello world")
