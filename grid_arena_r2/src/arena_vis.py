import cv2
from coordinates import cordinates

cap = cv2.VideoCapture(2)

# image = cv2.imread("prats.jpg")

while True:
    _, image = cap.read()

    for key in cordinates:
        cv2.circle(image, (cordinates[key][0], cordinates[key][1]+3), 2, 2, 2)
        #cv2.putText(image, str(key), tuple(cordinates[key]), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0,0,0), 1)

    cv2.imshow("image", image)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
