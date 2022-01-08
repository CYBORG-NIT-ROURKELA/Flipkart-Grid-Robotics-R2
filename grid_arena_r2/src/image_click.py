import cv2

cam = 2

def cam_index(cam):
    print("atya")
    print(cam)
    if cam_index == 2:
        return cv2.VideoCapture(cam)
    else:
        try:
            return cv2.VideoCapture(cam)
        except:
            cam -= 1
            return cam_index(cam)

cap = cam_index(cam)
print(cam)

while True:
    _, frame = cap.read()
    cv2.imwrite("image.png", frame)
    cv2.imshow("image", frame)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break

cap.release()
