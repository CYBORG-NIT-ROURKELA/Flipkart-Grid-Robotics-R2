import cv2


def load_coefficients(path):
    '''Loads camera matrix and distortion coefficients.'''
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]



# Load coefficients
mtx, dist = load_coefficients('calibration_chessboard.yml')
original = cv2.imread('image.jpg')

cv2.imwrite('undist.jpg', dst)

cap = cv.VideoCapture('/home/pranav/Videos/Webcam/sample.webm')
while(True):
    _, frame = cap.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    dst = cv2.undistort(original, mtx, dist, None, None)
    cv.imshow('image',frame)
    if cv.waitKey(1) and 0xFF == ord('q'):
        break

cv.destroyAllWindows()
cap.release()
