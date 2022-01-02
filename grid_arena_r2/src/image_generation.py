import cv2
import time
cap = cv2.VideoCapture(0)
i = 0
# while(i<10):
#     time.sleep(1)
#     print(i)
#     _, frame = cap.read()
#     frame = frame[60:420,0:640]
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('image',frame)
#     i+=1
#     if i == 10:
#         break
#     if cv2.waitKey(1) and 0xFF == ord('q'):
#         break
# i = 0
# print(i)
# _, frame = cap.read()
# frame=cv2.imread('sample_2.jpg')
# frame = frame[60:420,0:640]
# image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# reto, corners = cv2.findChessboardCorners(image, (7,6), None)
# cv2.imshow('image',frame)
while(True):

    print(i)
    _, frame = cap.read()
    # frame = frame[60:420,0:640]
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    reto, corners = cv2.findChessboardCorners(image, (8,6), None)
    cv2.imshow('image',frame)
    if reto == True:
        cv2.imwrite('gray/gray_'+str(i)+'.jpg', image)
        cv2.imwrite('frame/frame_'+str(i)+'.jpg', frame)
        i+=1
    if i == 1500:
         break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
