# import cv2 as cv
# import apriltag
# import glob
#
# cap = cv.VideoCapture(0)
# options = apriltag.DetectorOptions(families="tag36h11")
# detector = apriltag.Detector(options)
#
# criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#
# while(True):
#     _, frame = cap.read()
#     image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     # reto, corners = cv.findChessboardCorners(image, (7,6), None)
#     # if reto ==True:
#     #     corners2 = cv.cornerSubPix(image,corners, (11,11), (-1,-1), criteria)
#     #     print(corners2)
#     #     cv.drawChessboardCorners(frame, (7,6), corners2, reto)
#     #     cv.waitKey(100)
#     result = detector.detect(image)
#
#     if len(result):
#         x1, y1 = result[0].center
#         x1_1, y1_1 = result[0].corners[1]
#         x1_2, y1_2 = result[0].corners[2]
#         x1_3, y1_3 = result[0].corners[0]
#         x1_4, y1_4 = result[0].corners[3]
#
#         cv.circle(frame, (int(x1), int(y1)), 4, (255, 0, 0), -1)
#         cv.circle(frame, (int(x1_1), int(y1_1)), 4, (255, 0, 0), -1)
#         cv.circle(frame, (int(x1_2), int(y1_2)), 4, (255, 0, 0), -1)
#         cv.circle(frame, (int(x1_3), int(y1_3)), 4, (255, 0, 0), -1)
#         cv.circle(frame, (int(x1_4), int(y1_4)), 4, (255, 0, 0), -1)
#     cv.imshow('image',frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
# cv.destroyAllWindows()

# cv.destroyAllWindows()
# cap.release()
import time
import cv2 as cv
import os
import numpy as np
import glob
objp = np.zeros((8*6,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
imgpoints=[]
objpoints=[]
files = os.listdir('frame')
# cap = cv.VideoCapture('/home/pranav/Videos/Webcam/sample.webm')
import time
i=0
for file in files:
# while True:
    frame = cv.imread('frame/'+file)
    # _,frame=cap.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    reto, corners = cv.findChessboardCorners(image, (8,6), None)
    if reto == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(image,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, image.shape[::-1], None, None)
    print(dist)
    print(mtx)
    h,  w = frame.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
    print(newcameramtx)
    t = time.time()
    dst = cv.undistort(frame, mtx, dist, None, newcameramtx)
    print("time taken to process 1 frame : ", time.time()-t)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('result/result_'+str(i)+'.png', dst)
    i+=1
cv.destroyAllWindows()
