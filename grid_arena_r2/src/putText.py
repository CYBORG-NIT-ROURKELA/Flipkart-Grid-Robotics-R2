import cv2
from centroids import findRealCoordinates

image = cv2.imread('image1.png')

for i in range(15):
    for j in range(14):
        cv2.putText(image, str(i)+','+str(j), tuple(findRealCoordinates([i-0.09,j-0.09])), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)

cv2.imwrite('image_text.png', image)