#!/usr/bin/env python3

#Total delay: 216 ms
#Transmission delay: 33ms

import rospy
import socket
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import apriltag
import numpy as np

class DelayCalculator:
    def __init__(self):
        rospy.init_node('delay_calculator')
        rospy.Subscriber('/grid_robot/image_feed', Image, self.callback)
        

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bridge = CvBridge()
        self.detector = apriltag.Detector()

        rospy.loginfo("Code started")

        rospy.loginfo("Connected to 4210 : 192.168.158.178")

    def transmit(self, data):
        msg = "{}\r".format(data)
        rospy.loginfo(msg)

        self.sock.sendto(str.encode(msg), ('192.168.158.178', 4210))

    def callback(self, data):
        try:
            frame = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh_frame = cv2.threshold(gray_frame, 254, 255, cv2.THRESH_BINARY)

            results = self.detector.detect(gray_frame)

            for result in results:
                xc, yc = result.center
                x1, y1 = result.corners[1]
                x2, y2 = result.corners[2]

                for i in range(len(result.corners)):
                    x, y = result.corners[(i + 1) % 4]
                    cv2.putText(thresh_frame, str(i+1), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1, cv2.LINE_AA)

                print(cv2.countNonZero(thresh_frame))

                if cv2.countNonZero(thresh_frame) > 7500:
                    self.transmit(1)
                    print("Led detected")
                    rospy.signal_shutdown('led detected')
                else:
                    print("Led not detected")

                cv2.imshow("thresh", thresh_frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                rospy.signal_shutdown("user command")

        except CvBridgeError as e:
            print(e)


if __name__ == '__main__':
    dc = DelayCalculator()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
