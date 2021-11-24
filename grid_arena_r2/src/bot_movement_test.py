#!/usr/bin/env python3

import apriltag
# import argparse
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np
import math

from dynamic_reconfigure.server import Server
from grid_arena.cfg import pidConfig


class RobotsRelay:
    def __init__(self):
        rospy.init_node('robot_relay')

        self.sub = rospy.Subscriber('/grid_robot/image_feed', Image, self.callback)
        self.pub_error = rospy.Publisher('/grid_robot/error', UInt8, queue_size=10)
        self.pub_twist = rospy.Publisher('grid_robot/cmd_vel', Twist, queue_size=10)
        # self.pub_servo = rospy.Publisher('grid_robot/servo_angle', UInt8, queue_size=1)

        self.msg_twist = Twist()
        self.error_msg = UInt8()
        self.bridge = CvBridge()
        # self.msg_servo = UInt8()

        self.detector = apriltag.Detector()

        self.stage = 0
        self.thresh_dist = 30
        self.goal_array = [(263, 383), (93, 369), (263, 383), (264, 105)]

        self.intg, self.last_error = 0.0, 0.0
        srv = Server(pidConfig, self.dyn_callback)
        self.params = {'KP': 0.04, 'KD': 0.1, 'KI': 0, 'SP': 0.27}

    def dyn_callback(self, config, level):
        self.params = {k: config[k] for k in config if k != 'groups'}
        print(self.params)
        return config

    def pid(self, error, const):
        prop = error
        self.intg = error + self.intg
        diff = error - self.last_error
        balance = const['KP'] * prop + const['KI'] * self.intg + const['KD'] * diff
        self.last_error = error
        return balance

    def FollowNdRotate(self, error, angle_orientation_factor, linear_vel):

        ang_vel = self.pid(error, self.params)
        self.msg_twist.linear.x = linear_vel

        if -3.14 < angle_target < -1.57:
            if angle_orientation_factor > 0
                self.msg_twist.angular.z = ang_vel
                self.pub_error.publish(error)
            else:
                self.msg_twist.angular.z = -ang_vel
                self.pub_error.publish(-error)
        if -1.57 < angle_target < 0:
            if angle_orientation_factor > 0
                self.msg_twist.angular.z = -ang_vel
                self.pub_error.publish(-error)
            else:
                self.msg_twist.angular.z = ang_vel
                self.pub_error.publish(error)
        if 0 < angle_target < 1.57:
            if angle_orientation_factor > 0
                self.msg_twist.angular.z = ang_vel
                self.pub_error.publish(error)
            else:
                self.msg_twist.angular.z = -ang_vel
                self.pub_error.publish(-error)
        if 1.57 < angle_target < 3.14:
            if angle_orientation_factor > 0
                self.msg_twist.angular.z = ang_vel
                self.pub_error.publish(error)
            else:
                self.msg_twist.angular.z = -ang_vel
                self.pub_error.publish(-error)


    # def change_bot_count(self):
    #     if self.bot_count == 3:
    #         rospy.loginfo("Mission Accomplished")
    #         rospy.signal_shutdown("Mission Accomplished")
    #         return
    #
    #     self.bot_count += 1
    #     self.pub_twist = rospy.Publisher('grid_robot_{}/cmd_vel'.format(self.bot_count), Twist, queue_size=1)
    #     self.pub_servo = rospy.Publisher('grid_robot_{}/servo_angle'.format(self.bot_count), UInt8, queue_size=1)

    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            results = self.detector.detect(imgray)

            for result in results:
                if result.tag_id == self.bot_count + 1:
                    xc, yc = result.center
                    x1, y1 = result.corners[1]
                    x2, y2 = result.corners[2]
                    xm = (x1 + x2) / 2
                    xt, yt = self.goal_array[int((self.stage+1)/2)]
                    ym = (y1 + y2) / 2
                    xi, yi = self.goal_array[self.bot_count][int((self.stage+1)/2) - 1]

                    for i in range(len(result.corners)):
                        x, y = result.corners[(i + 1) % 4]
                        cv.putText(image, str(i+1), (int(x), int(y)), cv.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0), 1, cv.LINE_AA)

                    angle_target = math.atan2((yt - yi), (xt - xi))
                    cv.arrowedLine(image, (int(xi), int(yi)), (int(xt), int(yt)), (255, 0, 0), 2)

                    angle_bot = math.atan2((yc-ym),(xc-xm))
                    cv.arrowedLine(image, (int(xc), int(yc)), (int(xm), int(ym)), (0, 255, 0), 2)

                    m = math.tan(angle_target)
                    cross_track_error = (m*xc-yc+yi-m*xi)/(m**2+1)**0.5
                    angle_orientation_factor = (m*xm-ym+yc-m*xc)/(m**2+1)**0.5

                    euclidean_dist = np.linalg.norm(np.array([xc, yc]) - np.array([xt, yt]))
                    angle_error = abs(abs(angle_target) - abs(angle_bot))

                    cv.imshow('image', image)

                    while self.stage < len(self.goal_array):
                        if euclidean_dist > self.thresh_dist:
                            if angle_error > 0.25:
                                self.FollowNdRotate(angle_error, angle_orientation_factor, 0)
                            else:
                                self.FollowNdRotate(angle_error, angle_orientation_factor, self.params['SP'])
                        else:
                            self.stage += 1


                    self.pub_twist.publish(self.msg_twist)
                    # self.pub_servo.publish(self.msg_servo)

            if cv.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown("user command")

        except CvBridgeError as e:
            print(e)


if __name__ == '__main__':
    rr = RobotsRelay()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
            rospy.loginfo("shutdown...")
            msg = Twist()
            for i in range(100):
                rr.pub.publish(msg)
    except rospy.ROSInterruptException as e:
        print(e)
