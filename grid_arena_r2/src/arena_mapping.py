import cv2
import math
import time
import numpy as np
from matplotlib import pyplot as plt
image=cv2.imread('kj.png')
img_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred=img_grey
_,thrash=cv2.threshold(blurred,90,255, cv2.THRESH_BINARY)
cv2.imshow('frame',thrash)
cv2.waitKey(1000)
canny=cv2.Canny(thrash,240,255)
contours,_=cv2.findContours(thrash,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cord=[]
combined=[]
contour_value=[]
i=0
for contour in contours:
    approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    x=approx.ravel()[0]
    y=approx.ravel()[1]
    contour_value.append(len(approx))
    M = cv2.moments(contour)
    if M["m00"]:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    if(cv2.contourArea(contour)>=500 and cv2.contourArea(contour)<=1650):
        cord.append([cX,cY])
        i+=1
cordx = sorted(cord, key = lambda x: x[0])
final_cord=[]
for i in range(7):
    if(i%2==0):
        for j in range(2):
            a=cordx[:13]
            del(cordx[:13])
            a = sorted(a, key = lambda x: x[1])
            final_cord.append(a)
    else:
        for k in range(2):
            a=cordx[:7]
            del(cordx[:7])
            a = sorted(a, key = lambda y: y[1])
            final_cord.append(a)
# for c in final_cord:
#     for p in c:
#         cv2.drawMarker(image, tuple(p),(255,0,0), markerType=cv2.MARKER_CROSS, thickness=1)
#         cv2.imshow("image", image)
#         if cv2.waitKey(100) == 27:
#             cv2.destroyAllWindows()
#             break
final_cordinates={}
k=0
for i in range(14):
    # print(final_cordinates)
    if(len(final_cord[i])==13):
        for j in range(13):
            final_cordinates[(i+1,j)]=final_cord[i][12-j]
    else:
        for j in range(7):
            a=[0,1,4,5,8,9,12]
            final_cordinates[(i+1, a[j])] = final_cord[i][6-j]
print(final_cordinates)
