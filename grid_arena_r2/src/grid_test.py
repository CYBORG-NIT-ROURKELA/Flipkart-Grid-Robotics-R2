import cv2



cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()
  
    cv2.imshow("frame", frame)
    cv2.imwrite("pranav.png",frame)



    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()