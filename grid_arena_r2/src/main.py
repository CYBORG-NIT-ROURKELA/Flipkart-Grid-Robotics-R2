#!/usr/bin/env python

import apriltag
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv

class Main:
    def __init__(self):
        rospy.init_node('keyboard_teleop', anonymous=True)
        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
        self.pub = rospy.Publisher('/grid_robot/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)
        self.msg = Twist()
        self.bridge = CvBridge()
        self.destinations = {'Mumbai':(295,227) , 'Delhi':(570,227)     , 'Kolkata':  (850,227), 
                             'Chennai':(230,360),'Bengaluru':(500,360)  , 'Hyderabad':(780,360), 
                             'Pune':(230,610)   , 'Ahemadabad':(500,610), 'Jaipur':   (780,610),
                             'Induct1':(92,227) }

        self.toDestination=True

    def callback(self, data):

        def turnRight(y1,y2):
            if y1>=y2-20:
                self.msg.angular.z = 0
                return True
            else:
                print("90-Turn")
                self.msg.angular.z = -1 #- => Right
                return False

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            img = cv_image.copy()

            ### Destination Markings
            cv.circle(img, self.destinations['Induct1'], 7, (0, 255, 255), -1)

            cv.circle(img, self.destinations['Mumbai'], 7, (0, 255, 255), -1)
            cv.circle(img, self.destinations['Delhi'], 7, (0, 255, 255), -1)
            cv.circle(img, self.destinations['Kolkata'], 7, (0, 255, 255), -1)
            
            cv.circle(img, self.destinations['Chennai'], 7, (0, 255, 255), -1)
            cv.circle(img, self.destinations['Pune'], 7, (0, 255, 255), -1)

            cv.circle(img, self.destinations['Bengaluru'], 7, (0, 255, 255), -1)
            cv.circle(img, self.destinations['Ahemadabad'], 7, (0, 255, 255), -1)

            cv.circle(img, self.destinations['Hyderabad'], 7, (0, 255, 255), -1)
            cv.circle(img, self.destinations['Jaipur'], 7, (0, 255, 255), -1)


            ### BOT DETECTION
            image = cv_image
            imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # gray version

            detector = apriltag.Detector()
            result = detector.detect(imgray)
            # print(result)
            x0, y0 = result[0].center
            x1, y1 = result[0].corners[1] #LEFT
            x2, y2 = result[0].corners[2] #RIGHT
            cv.circle(img, (int(x0), int(y0)), 7, (255, 255, 255), -1)
            cv.circle(img, (int(x1), int(y1)), 7, (0, 0, 0), -1)
            cv.circle(img, (int(x2), int(y2)), 7, (255, 255, 255), -1)

         
            ### BOT MOVEMENT
            bot1_destination = self.destinations['Bengaluru']
            x = bot1_destination[0]; y = bot1_destination[1]
            # print(x0,x-35)
            xvel = 0

            ## Getting to Destination
            if self.toDestination:
                if x0<x-35:
                    xvel = 0.2
                else:
                    turned = turnRight(y1,y2)
                    if turned and y0<y:
                        xvel = 0.2
            

            
            
            cv.imshow('image', img)
        except CvBridgeError as e:
            print(e)
        
        
        
        k = cv.waitKey(1) & 0xFF

        if k == 27:
            rospy.signal_shutdown("shutdown")
            cv.destroyAllWindows()

        self.msg.linear.x = xvel
        self.pub.publish(self.msg)
        self.rate.sleep()

if __name__ == '__main__':
    kt = Main()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
