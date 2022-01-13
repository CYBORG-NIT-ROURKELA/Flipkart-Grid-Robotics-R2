import cv2
import numpy as np
from matplotlib import pyplot as plt
img=cv2.imread('arena.jpg')
img_grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(img_grey,(5,5),0)
_,thrash=cv2.threshold(blurred,240,255, cv2.THRESH_BINARY)
canny=cv2.Canny(thrash,240,255)
cv2.imshow("new_one",canny)
contours,_=cv2.findContours(thrash,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.imshow("new",blurred)
x_c=[]
y_c=[]
contour_value=[]
area=[]
i=1
for contour in contours:
    approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    cv2.drawContours(img, [approx],0,(0,0,0),2)
    x=approx.ravel()[0]
    y=approx.ravel()[1]
    contour_value.append(len(approx))
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    x_c.append(cX)
    y_c.append(cY)
    cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
    a=cv2.contourArea(contour)
    area.append(a)
final=list(zip(contour_value,x_c,y_c,area))
final.sort()
print(final)
cv2.line(img,(final[1][1],final[1][2]),(final[0][1],final[0][2]),(0,0,0),1)
cv2.line(img,(final[0][1],final[0][2]),(final[2][1],final[2][2]),(0,0,0),1)
cv2.line(img,(final[2][1],final[2][2]),(final[3][1],final[3][2]),(0,0,0),1)
cv2.line(img,(final[3][1],final[3][2]),(final[5][1],final[5][2]),(0,0,0),1)
cv2.line(img,(final[5][1],final[5][2]),(final[6][1],final[6][2]),(0,0,0),1)
cv2.line(img,(final[6][1],final[6][2]),(final[8][1],final[8][2]),(0,0,0),1)
cv2.line(img,(final[8][1],final[8][2]),(final[7][1],final[7][2]),(0,0,0),1)
cv2.putText(img, "1", (final[1][1]-80,final[1][2]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "2", (final[0][1]-80,final[0][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "3", (final[2][1]-100,final[2][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "4", (final[3][1]-110,final[3][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "5", (final[5][1]-80,final[5][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "6", (final[6][1]-80,final[6][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "7", (final[8][1]-80,final[8][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(img, "8", (final[7][1]-80,final[7][2]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.imshow("new_1",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
