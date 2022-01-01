#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import time
import numpy as np
from schedule import find_schedule
from centroids import findCoordinates
from destination import give_destination





# schedule = find_schedule([0,8],[11,4],[0,4],[8,9])
# agent0_path = findCoordinates(schedule,"agent0")
# agent1_path = findCoordinates(schedule,"agent1")


class Planned_path:

    def __init__(self):
        rospy.init_node('plan_path')
        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
        
        self.bridge = CvBridge()
        self.m = self.n = 0
        self.dock1 = [0,4]
        self.dock2 = [0,9]
        self.station1,self.station2 = give_destination('/home/adyasha/Desktop/Sample Data - Sheet1.csv')

        
        
        
    def callback(self, data):
        try:


            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            img = cv_image.copy()
            image = cv_image.copy()
            cv.imshow('image', image)
            cv.imshow('img', img)

        except CvBridgeError as e:
            print(e)

        if cv.waitKey()==27:                    # ESC to end program
            rospy.signal_shutdown("shutdown")
            cv.destroyAllWindows()

        # k = cv.waitKey(0) & 0xFF 
       
       

if __name__ == '__main__':
    pps = Planned_path()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
