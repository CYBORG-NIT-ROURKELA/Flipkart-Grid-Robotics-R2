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
import time

from utils import detect_apriltag, error_calculation

# from dynamic_reconfigure.server import Server
# from grid_arena.cfg import pidConfig

detector = apriltag.Detector()

class BotManeuver:
    def __init__(self, goal_array):

        rospy.init_node("bot_maneuver")

        self.sub = rospy.Subscriber('grid_robot/image_feed', Image, self.callback)
        self.pub_twist = rospy.Publisher('grid_robot_0/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)

        #parameters
        self.thresh_dist = 19
        self.rotation_param = 32
        self.rotation_param_2 = 1
        self.thresh_rotn = 0.5

        self.msg_twist = Twist()
        self.bridge = CvBridge()


        self.stage = 0
        self.tag_id = 2
        # self.thresh_dist = 30
        self.goal_array = goal_array

        self.intg, self.last_error = 0.0, 0.0
        self.params = {'KP': 0.0093, 'KD': 0.1, 'KI': 0, 'SP': 0.27}

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
        self.pub_twist.publish(self.msg_twist)
        print("stopped")

    def FollowStraight(self, xt, xc, euclidean_dist, angle_target, cross_track_error, error, linear_vel):
        if euclidean_dist > self.thresh_dist:
            ang_vel = 0

            if error > 3.14:
                ang_vel = self.pid(self.rotation_param*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(self.rotation_param*(error+6.28), self.params)
            else:
                ang_vel = self.pid(self.rotation_param*error, self.params)


            # if 1.05 < angle_target <= 1.57:
            #     ang_vel = self.pid(-self.rotation_param_2*cross_track_error, self.params)
            # elif 1.57 < angle_target < 2.09:
            #     ang_vel = self.pid(cross_track_error, self.params)
            #
            # elif -2.09 < angle_target <= -1.57:
            #     ang_vel = self.pid(self.rotation_param_2*cross_track_error, self.params)
            # elif -1.57 < angle_target < -1.05:
            #     ang_vel = self.pid(-self.rotation_param_2*cross_track_error, self.params)
            #
            # elif -0.523 < angle_target < 0.523:
            #     ang_vel = self.pid(-self.rotation_param_2*cross_track_error, self.params)
            #
            # elif -3.15 < angle_target < -2.617:
            #     ang_vel = self.pid(-self.rotation_param_2*cross_track_error, self.params)
            # elif 2.617 < angle_target < 3.15:
            #     ang_vel = self.pid(self.rotation_param_2*cross_track_error, self.params)

            self.msg_twist.linear.x = linear_vel
            self.msg_twist.angular.z = ang_vel
            print("Following...Linear velocity: {}; Angular velocity: {}".format(linear_vel, ang_vel))
        else:
            self.stop()
            if self.stage < len(self.goal_array)-2:
                self.stage += 1
            if self.stage == len(self.goal_array)-1:
                self.stop()
                rospy.signal_shutdown("Maneuver done")

    def Rotate(self, error, abs_angle_diff):
        if abs_angle_diff > self.thresh_rotn:
            if error > 3.14:
                ang_vel = self.pid(self.rotation_param*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(self.rotation_param*(error+6.28), self.params)
            else:
                ang_vel = self.pid(self.rotation_param*error, self.params)

            if self.msg_twist.linear.x == 0:
                if ang_vel < 0:
                    ang_vel = -1.2963
                else:
                    ang_vel = 1.2963

            # self.msg_twist.linear.x = 0
            self.msg_twist.angular.z = ang_vel
            print("Rotating...Angular velocity: {} abs_angle_diff: {}".format(ang_vel, abs_angle_diff))
        else:
            self.stop()


    #xt: x coordinate of target point
    #xc: x coordinate of center of bot
    #abs_angle_diff  = abs(abs(desired orientation of bot)-abs(current orientation of bot))
    #error = desired orientation of bot - current orientation of bot
    #euclidean_dist = real time distance between bot center and target coordinate
    #angle_target = desired orientation of bot
    #cross_track_error = perpendicular distance of center of bot from the line joining the initial and target coordinates

    def maneuver(self, xt, xc, abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error):
        if abs_angle_diff > self.thresh_rotn:
            self.Rotate(error, abs_angle_diff)
        else:
            # self.stop()
            self.FollowStraight(xt, xc, euclidean_dist, angle_target, cross_track_error, error, 0.06)

    def callback(self, data):
        try:
            #recieving image
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            #detecting apriltag
            results = detect_apriltag(image, detector, self.tag_id)
            if results is None or self.goal_array is None:
                pass
            else:
                if len(results):
                    xc, yc = results[0].center
                    x1, y1 = results[0].corners[1]
                    x2, y2 = results[0].corners[2]
                    xm = (x1 + x2) / 2
                    ym = (y1 + y2) / 2

                    xt, yt = self.goal_array[int(self.stage)]
                    xi, yi = self.goal_array[int(self.stage) - 1]

                    if self.stage < len(self.goal_array):
                        cv.arrowedLine(image, (int(xi), int(yi)), (int(xt), int(yt)), (255, 0, 0), 2)
                        cv.arrowedLine(image, (int(xc), int(yc)), (int(xm), int(ym)), (0, 255, 0), 2)

                        abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error = error_calculation(yi, yt, xt, xi, yc, ym, xc, xm)

                        self.maneuver(xt, xc, abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error)

                        cv.imshow("frame", image)

                    self.pub_twist.publish(self.msg_twist)

            if cv.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown("user command")

        except CvBridgeError as e:
            print(e)

if __name__ == '__main__':
    bm = BotManeuver(goal_array=[(213, 199), (212, 222), (210, 247), (234, 247), (254, 247), (274, 246), (295, 246), (314, 248), (334, 246), (213, 175)]) #(210, 247), (334, 247)
    #(225, 287), (225, 335), (265, 384), (324, 384), (350, 335), (350, 287), (324, 230), (265, 235)]
    #
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
