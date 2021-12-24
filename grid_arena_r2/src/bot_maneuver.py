#!/usr/bin/env python3

import apriltag
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np
import math

from utils import detect_apriltag, error_calculation

from dynamic_reconfigure.server import Server
from grid_arena.cfg import pidConfig

class BotManeuver:
    def __init__(self):

        rospy.init_node("bot_maneuver")

        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
        self.pub_twist = rospy.Publisher('grid_robot/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)

        self.msg_twist = Twist()
        self.bridge = CvBridge()


        self.stage = 0
        # self.thresh_dist = 30
        self.goal_array = [(281, 265), (331, 265), (331, 216), (281, 216), (281, 265), (231, 265)]

        self.intg, self.last_error = 0.0, 0.0
        self.params = {'KP': 0.04, 'KD': 0.1, 'KI': 0, 'SP': 0.27}

    def pid(self, error, const):
        prop = error
        self.intg = error + self.intg
        diff = error - self.last_error
        balance = const['KP'] * prop + const['KI'] * self.intg + const['KD'] * diff
        self.last_error = error
        return balance

    def stop(self):
        self.msg_twist.linear.x = 0
        self.msg_twist.angular.z = 0
        print("stopped")

    def FollowStraight(self, euclidean_dist, linear_vel):
        if euclidean_dist > 15:
            self.msg_twist.linear.x = linear_vel
        else:
            self.stop()
            self.stage += 1

    def Rotate(self, error, abs_angle_diff):
        if abs_angle_diff > 0.1:
            if error > 3.14:
                ang_vel = self.pid(20*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(20*(error+6.28), self.params)
            else:
                ang_vel = self.pid(20*error, self.params)
        else:
            ang_vel = 0

        self.msg_twist.angular.z = ang_vel
        print(ang_vel)

    def maneuver(self, abs_angle_diff, error, euclidean_dist):
        if abs_angle_diff > 0.1:
            self.Rotate(error, abs_angle_diff)
            self.FollowStraight(euclidean_dist, 0)
        else:
            self.Rotate(error, abs_angle_diff)
            self.FollowStraight(euclidean_dist, 0.27)

    def callback(self, data):
        try:
            #recieving image
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            #detecting apriltag
            results = detect_apriltag(image)

            if len(results):
                xc, yc = results[0].center
                x1, y1 = results[0].corners[1]
                x2, y2 = results[0].corners[2]
                xm = (x1 + x2) / 2
                ym = (y1 + y2) / 2

                xt, yt = self.goal_array[int(self.stage)]
                xi, yi = self.goal_array[int(self.stage) - 1]

                if self.stage < len(self.goal_array)-1:
                    cv.arrowedLine(image, (int(xi), int(yi)), (int(xt), int(yt)), (255, 0, 0), 2)
                    cv.arrowedLine(image, (int(xc), int(yc)), (int(xm), int(ym)), (0, 255, 0), 2)
                    cv.imshow("frame", image)
                    abs_angle_diff, error, euclidean_dist = error_calculation(yi, yt, xt, xi, yc, ym, xc, xm)
                    self.maneuver(abs_angle_diff, error, euclidean_dist)

                self.pub_twist.publish(self.msg_twist)

            if cv.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown("user command")

        except CvBridgeError as e:
            print(e)

if __name__ == '__main__':
    bm = BotManeuver()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
