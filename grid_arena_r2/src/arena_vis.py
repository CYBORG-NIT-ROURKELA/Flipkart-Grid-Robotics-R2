from coordinates import cordinates
import cv2

param = {'map':{'dimensions' : [15,14],'obstacles' : [(0,0),(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),(0,12),(0,13),(3, 2), (4, 2), (3, 3), (4, 3), (7, 2), (8, 2), (7, 3), (8, 3), (11, 2), (12, 2), (11, 3), (12, 3), (3, 6), (4, 6), (3, 7), (4, 7), (3, 10), (4, 10), (3, 11), (4, 11), (7, 6), (8, 6), (7, 7), (8, 7), (7, 10), (8, 10), (7, 11), (8, 11), (11, 6), (12, 6), (11, 7), (12, 7), (11, 10), (12, 10), (11, 11), (12, 11)]
    }}

cap = cv2.VideoCapture(0)

while 1:
    _, frame = cap.read()
    if _:
        for key in cordinates:
            cv2.circle(frame, tuple(cordinates[key]), 3, (255,0,121), 3)
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            break
    else:
        pass

