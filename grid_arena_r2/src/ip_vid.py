import cv2
import numpy as np

cap = cv2.VideoCapture('vid.mp4')

def blank(x):
    pass

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H", "Trackbars", 0, 255, blank)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, blank)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, blank)
cv2.createTrackbar("U-H", "Trackbars", 0, 255, blank)
cv2.createTrackbar("U-S", "Trackbars", 0, 255, blank)
cv2.createTrackbar("U-V", "Trackbars", 0, 255, blank)

if cap.isOpened() == False:
    print("Error in opening video...")

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-S", "Trackbars")
        l_v = cv2.getTrackbarPos("L-V", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower, upper)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('Video', frame)
        # cv2.imshow('HSV_Video', hsv)
        # cv2.imshow('Mask', mask)
        cv2.imshow('Final_Video', result)

        if cv2.waitKey(25) and 0xFF == ord('q'):
            break

    else:
        cap.open('vid.mp4')
cap.release()
cv2.destroyAllWindows()
