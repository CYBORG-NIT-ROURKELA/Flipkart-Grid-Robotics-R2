import cv2

cap = cv2.VideoCapture(2)
start_x = 51
start_y = 460
d_x = 37
d_y = 37
while True:
    ret, frame = cap.read()
    # if ret:
    #     print("frame fixed")
    #     # cv2.circle(frame, (start_x,start_y), 1, (255, 0, 0), 1)
    
    for i in range (0,15):
        for j in range (0,14):
            x = int(start_x + i*d_x)
            y = int(start_y - j*d_y)
            cv2.drawMarker(frame, (x,y), (0,255,0), 1, 6, 1)
        
            j+=1
        i+=1
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == 27:
        break
    
cap.release()
cv2.destroyAllWindows()