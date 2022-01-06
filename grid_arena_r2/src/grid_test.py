import cv2

from gopro_params import fix_feed

cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()
    frame = fix_feed(frame)
    cv2.imshow("frame", frame)

    working_frame = frame.copy()



    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()