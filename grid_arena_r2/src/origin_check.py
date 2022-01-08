import cv2 as cv
cap = cv.VideoCapture(0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
imgpoints=[]
objpoints=[]
i=0
while True:
    _, frame = cap.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    reto, corners = cv.findChessboardCorners(image, (7,6), None)
    # h,  w = frame.shape[:2]
    # newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, image.shape[::-1], None, None)
    if reto == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(image,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
    cv.imshow('image',img)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break
cv.destroyAllWindows()
