import cv2

from gopro_params import fix_feed,real_coords

cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()
    frame = fix_feed(frame)
    
    for i in range(15):
        for j in range(2):
            
            d = (i,j)
            coord = real_coords[d]
            # cv2.circle(frame,tuple(coord),1,(255,0,0),1)
            cv2.drawMarker(frame, tuple(coord), (255,255,0), 0, 6, 1)
            j+=1
    i+=1
    cv2.imshow("frame", frame)

   



    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()