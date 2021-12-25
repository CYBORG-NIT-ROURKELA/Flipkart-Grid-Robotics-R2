#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import csv
import numpy as np
from schedule import find_schedule
from centroids import findCoordinates
from destination import give_destination


dock1 = [0,4]
dock2 = [0.9]
station1,station2 = give_destination('/home/adyasha/Desktop/Sample Data - Sheet1.csv')
print(station1[1])
print(len(station2))


schedule = find_schedule([0,8],[11,4],[0,4],[8,9])
agent0_path = findCoordinates(schedule,"agent0")
agent1_path = findCoordinates(schedule,"agent1")




class Planned_path:
    m=n=0
    def __init__(self):
        rospy.init_node('plan_path')
        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
        
        self.bridge = CvBridge()
        self.m = self.n = 0
        
        
        
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            img = cv_image.copy()
            image = cv_image.copy()
            
            dest1 = station1[self.m]
            dest2 = station2[self.n]
            start1 = dock1
            start2 = dock2

            while(m<141 and n<141):
                i=j=0
                goal1 = dest1[2]

                goal2 = dest2[2]
                schedule = find_schedule(start1,goal1,start2,goal2)
                agent0_path = findCoordinates(schedule,"agent0")
                agent1_path = findCoordinates(schedule,"agent1")


            
                i_end = len(agent0_path)-1
                j_end = len(agent1_path)-1

                agent0_last = agent0_path[len(agent0_path)-1]
                agent1_last = agent1_path[len(agent1_path)-1]
                agent0_state = agent0_path[i]
                agent1_state = agent1_path[j]
                
            


                while agent0_state!=agent0_last or agent1_state!=agent1_last:
                    if i!=i_end:
                        
                        image = cv.arrowedLine(image, (agent0_state["x_c"],agent0_state["y_c"]), (agent0_path[i+1]["x_c"],agent0_path[i+1]["y_c"]),
                                            (0,255,0), 4)
                        

                    if j!=j_end:

                        image = cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_path[j+1]["x_c"],agent1_path[j+1]["y_c"]),
                                            (0,0,255), 4)
                        

                    if i!=i_end:
                        i+=1
                    if j!=j_end:
                        j+=1
                    agent0_state = agent0_path[i]
                    agent1_state = agent1_path[j]
                m+=1
                n+=1
                        
                crop_image = image[112:654, 287:909]
                cv.imshow('image', image)
                cv.imshow('img', img)
                cv.imshow('cropped',crop_image)

        except CvBridgeError as e:
            print(e)

        k = cv.waitKey(0) & 0xFF 
       
       

if __name__ == '__main__':
    pps = Planned_path()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
