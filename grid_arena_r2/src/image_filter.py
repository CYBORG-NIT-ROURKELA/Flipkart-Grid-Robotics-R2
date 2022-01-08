import time
import cv2 as cv
import os
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
i =0
while(i<500):
    if os.path.exists('frame/frame_'+str(i)+'.jpg'):
        frame = cv.imread('frame/frame_'+str(i)+'.jpg')
        image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        reto, corners = cv.findChessboardCorners(image, (7,6), None)
        if reto ==True:
            corners2 = cv.cornerSubPix(image,corners, (11,11), (-1,-1), criteria)
            cv.drawChessboardCorners(frame, (7,6), corners2, reto)
            # time.sleep(2)
        else:
            os.remove('frame/frame_'+str(i)+'.jpg')
        cv.imshow('image',frame)

        if cv.waitKey(1) and 0xFF == ord('q'):
            break
    i+=1
cv.destroyAllWindows()
