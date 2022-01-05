#!/usr/bin/env python3

import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
import apriltag
import rospy
from sensor_msgs.msg import Image
import time
t=time.time()
bridge = CvBridge()
detector = apriltag.Detector()
print(time.time()-t)
def callback(data):
    frame = bridge.imgmsg_to_cv2(data)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    result = detector.detect(gray)

    if result is not None and len(result):
        x1, y1 = result[0].center
        x1_1, y1_1 = result[0].corners[1]
        x1_2, y1_2 = result[0].corners[2]
        x1_3, y1_3 = result[0].corners[0]
        x1_4, y1_4 = result[0].corners[3]

        cv.circle(frame, (int(x1), int(y1)), 4, (255, 0, 0), -1)
        cv.circle(frame, (int(x1_1), int(y1_1)), 4, (255, 0, 0), -1)
        cv.circle(frame, (int(x1_2), int(y1_2)), 4, (255, 0, 0), -1)
        cv.circle(frame, (int(x1_3), int(y1_3)), 4, (255, 0, 0), -1)
        cv.circle(frame, (int(x1_4), int(y1_4)), 4, (255, 0, 0), -1)

    cv.imshow('image', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        rospy.signal_shutdown('exit')

if __name__ == '__main__':
    rospy.init_node('demo')
    rospy.Subscriber('grid_robot/image_feed', Image, callback)
    try:
        rospy.spin()
    except ROSInterruptException as e:
        print(e)
    cv.destroyAllWindows()
