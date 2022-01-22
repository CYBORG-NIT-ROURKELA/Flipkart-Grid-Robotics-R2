import cv2
import numpy as np

frame = cv2.imread("image_2.png")
frame = cv2.resize(frame, (640, 480))
image_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

cv2.imshow("frame", frame)

while True:
    mask = cv2.inRange(image_HSV, np.array([128, 28, 246]), np.array([255, 255, 255]))
    mask_1 = cv2.inRange(image_HSV, np.array([0, 0, 0]), np.array([255, 0, 255]))

    output = cv2.bitwise_and(frame, frame, mask = mask)
    output_1 = cv2.bitwise_and(frame, frame, mask = mask_1)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    output_1 = cv2.cvtColor(output_1, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_1, hierarchy_1 = cv2.findContours(output_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for contour in contours:
    #     C = cv2.moments(contour)
    #
    #     cX = int(C['m10']/(C['m00']+1e-4))
    #     cY = int(C['m01']/(C['m00']+1e-4))
    #
    #     cv2.circle(frame, (cX, cY), 2, (0, 0, 255), -1)

    # for contour_1 in contours_1:
    #     C = cv2.moments(contour_1)
    #
    #     cX = int(C['m10']/(C['m00']+1e-4))
    #     cY = int(C['m01']/(C['m00']+1e-4))
    #
    #     cv2.circle(frame, (cX, cY), 2, (0, 0, 255), -1)

    # cv2.imshow("frame", frame)
    # cv2.imshow("white mask", output_1)
    # cv2.imshow("blue mask", output)

    if cv2.waitKey(25) and 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
