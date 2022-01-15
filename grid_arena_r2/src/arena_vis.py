import cv2
from coordinates import cordinates

image = cv2.imread("prats.jpg")

for key in cordinates:
    cv2.circle(image, tuple(cordinates[key]), 2, 2, 2)
    cv2.putText(image, str(key), tuple(cordinates[key]), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0,0,0), 1)
    cv2.imshow("image", image)
    cv2.waitKey(200)
cv2.destroyAllWindows()
