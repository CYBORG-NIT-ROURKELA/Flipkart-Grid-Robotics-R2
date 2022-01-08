#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np

class ImageFeed:
    def __init__(self):
        rospy.init_node('cam_driver')
        self.pub = rospy.Publisher('grid_robot/image_feed', Image, queue_size=1)
        self.rate = rospy.Rate(2000) #10Hz
        self.msg = Image()
        self.bridge = CvBridge()
        rospy.loginfo("Camera Driver Started")

    def read(self, device_index):
        cap = cv.VideoCapture(device_index, cv.CAP_V4L)
        while not rospy.is_shutdown() and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # dist=np.array([[-0.25378681 , 0.02657608 , 0.0302187 , -0.00403553 , 0.046275 ,]])
                # old_mtx=np.array([[ 387.51367505   , 0.,          318.92583391],
                #                   [   0.    ,      393.26409928  ,237.04613992],
                #                   [   0.     ,       0.    ,        1.        ]])
                # new_mtx=np.array([[ 335.03356934 ,   0. ,         313.84161596],
                #                   [   0.   ,       346.29098511 , 257.87514082],
                #                   [   0.     ,       0.      ,      1.        ]])

                # frame  = cv.undistort(frame, old_mtx, dist, None, new_mtx)
                # cv.imshow('image', frame)
                if cv.waitKey(0) & 0xFF == ord('q'):
                    break
                self.msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
                self.publish()
            else:
                cap.open(device_index)
        cap.release()
        cv.destroyAllWindows()

    def publish(self):
        self.pub.publish(self.msg)


if __name__ == '__main__':
    try:
        image_feed = ImageFeed()
        image_feed.read(0)
    except rospy.ROSInterruptException as e:
        print(e)
