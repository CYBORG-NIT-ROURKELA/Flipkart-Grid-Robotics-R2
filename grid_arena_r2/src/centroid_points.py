import cv2

from gopro_params import fix_feed

cap = cv2.VideoCapture(2)
start_x = 157
start_y = 444
d_x = 23
d_y = 21
while True:
    ret, frame = cap.read()
    image = fix_feed(frame)

    # if ret:
    #     print("frame fixed")
    #     # cv2.circle(frame, (start_x,start_y), 1, (255, 0, 0), 1)
   
    


        
    
    
        for i in range (0,14):


            for j in range (0,13):
                print(i,j)

                x = start_x + i*d_x
                y = start_y - j*d_y
            
                cv2.drawMarker(frame, (x,y), 1, (255, 0, 0), 1)
            
                j+=1
            i+=1
    cv2.imshow("frame", frame)
    cv2.imshow("frame2", image)
    




    if cv2.waitKey(1) == 27:

        break
    
cap.release()
cv2.destroyAllWindows()