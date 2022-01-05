import cv2 as cv
# import globe
import os
import time
import numpy as np
import apriltag
import time
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
# back-up using noiseplay cam matrix
dist=np.array([[-0.25378681 , 0.02657608 , 0.0302187 , -0.00403553 , 0.046275 ,]])
old_mtx=np.array([[ 387.51367505   , 0.,          318.92583391],
 [   0.    ,      393.26409928  ,237.04613992],
 [   0.     ,       0.    ,        1.        ]])
new_mtx=np.array([[ 335.03356934 ,   0. ,         313.84161596],
 [   0.   ,       346.29098511 , 257.87514082],
 [   0.     ,       0.      ,      1.        ]])
# dist=np.array([[ -5.0687763545159947e-01, 1.5526537849584250e+00,
#  4.3319391883287345e-03, -8.2244142017397024e-03,
#  -8.2557449787826123e+00 ]])
# old_mtx=np.array([[  2.94448937e+03,   0.00000000e+00,   3.53420640e+02],
#  [  0.00000000e+00,   1.84028833e+03,   2.56651780e+02],
#  [  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
# new_mtx=np.array([[  2.52488098e+03,   0.00000000e+00,   3.11585980e+02],
#  [  0.00000000e+00,  0.97818140e+03,   2.22609825e+02],
#  [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
# cap = cv.VideoCapture('/home/pranav/Videos/Webcam/sample.webm')
cap = cv.VideoCapture(2)
while(True):
    _, image = cap.read()
    # image = image[60:420:0:640]
    cv.imshow('raw',image)
    t=time.time()
    dst = cv.undistort(image, old_mtx, dist, None, new_mtx)
    print('time taken to undistort :',time.time()-t)
    image = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    result = detector.detect(image)
    if len(result):
        x1, y1 = result[0].center
        x1_1, y1_1 = result[0].corners[1]
        x1_2, y1_2 = result[0].corners[2]
        x1_3, y1_3 = result[0].corners[0]
        x1_4, y1_4 = result[0].corners[3]

        cv.circle(dst, (int(x1), int(y1)), 4, (255, 0, 0), -1)
        cv.circle(dst, (int(x1_1), int(y1_1)), 4, (255, 0, 0), -1)
        cv.circle(dst, (int(x1_2), int(y1_2)), 4, (255, 0, 0), -1)
        cv.circle(dst, (int(x1_3), int(y1_3)), 4, (255, 0, 0), -1)
        cv.circle(dst, (int(x1_4), int(y1_4)), 4, (255, 0, 0), -1)
    cv.imshow('result',dst)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break
cv.destroyAllWindows()
cap.release()
