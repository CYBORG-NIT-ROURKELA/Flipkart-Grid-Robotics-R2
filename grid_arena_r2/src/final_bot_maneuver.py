#! /usr/bin/env python

import rospy
import actionlib
from grid_arena_r2.msg import botAction, botFeedback, botResult
import argparse
import apriltag
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np
import math
import time

from utils import detect_apriltag, error_calculation

from dynamic_reconfigure.server import Server
# from grid_arena.cfg import pidConfig

class BotManeuver:
    _feedback = botFeedback()
    _result = botResult()

    def __init__(self, name, args):
        self._action_name = str(name)+'_'+str(args.tag_id)

        print(self._action_name)

        #Publisher
        self.pub_twist = rospy.Publisher('grid_robot_{}/cmd_vel'.format(args.tag_id), Twist, queue_size=10)
        self.pub_servo = rospy.Publisher('grid_robot_{}/servo_angle'.format(args.tag_id), Int64, queue_size = 1)

        #multiplying factor
        self.rotation_param = 32

        #PID Parameters for the bots
        if args.tag_id == 1: #PCB marked 1
            self.params = {'KP': 0.59, 'KD': 4.7, 'KI': 0, 'SP': 0.6}
        elif args.tag_id == 7: #PCB Marked 2
            self.params = {'KP': 0.64, 'KD': 4.6, 'KI': 0, 'SP': 0.6}

        #msgs
        self.msg_twist = Twist()
        self.bridge = CvBridge()

        self.stage = 0

        #tag id
        self.tag_id = args.tag_id
        print(self.tag_id)

        #Threshold distance for bot halting
        self.thresh_dist = 8

        self.dropped = False
        self.drop_count = 0

        #apriltag detector
        self.detector = apriltag.Detector()

        self.goal_array = None
        self.prev_goal = None
        self.image = None

        self.intg, self.last_error = 0.0, 0.0

        #action server
        self._as = actionlib.SimpleActionServer(self._action_name, botAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        print('action server {} started'.format(args.tag_id))

        #Subscriber
        self.sub = rospy.Subscriber('grid_robot/image_feed', Image, self.callback)

        #Success Flag
        self.success = False

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

    #error = desired orientation of bot - current orientation of bot
    #euclidean_dist = real time distance between bot center and target coordinate

    def FollowStraight(self, euclidean_dist, error, linear_vel):

        if euclidean_dist > self.thresh_dist:
            #PID Logic
            if error > 3.14:
                ang_vel = self.pid(self.rotation_param*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(self.rotation_param*(error+6.28), self.params)
            else:
                ang_vel = self.pid(self.rotation_param*error, self.params)


            self.msg_twist.linear.x = linear_vel
            self.msg_twist.angular.z = ang_vel

            self.pub_servo.publish(0)

        else:
            self.stop()
            print("reached target coordinate")
            self.dropped = False
            self.success = True

    def Rotate(self, error, abs_angle_diff):
        if abs_angle_diff > 0.55:
            if error > 3.14:
                ang_vel = self.pid(self.rotation_param*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(self.rotation_param*(error+6.28), self.params)
            else:
                ang_vel = self.pid(self.rotation_param*error, self.params)

            if ang_vel > 0:
                ang_vel = 1.5
            else:
                ang_vel = -1.5

            self.msg_twist.linear.x = 0
            self.msg_twist.angular.z = ang_vel

        else:
            self.stop()
            if self.drop_count == 0:
                self.stop()
                self.pub_servo.publish(1)
                self.drop_count += 1
            else:
                self.stop()
                rospy.sleep(2)
                self.pub_servo.publish(0)
                self.dropped = False
                self.drop_count = 0
                self.success = True

    def callback(self, data):
        try:
            #recieving image
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            cv.imshow("fast_n_furious_{}".format(self.tag_id), image)
            #detecting apriltag
            results = detect_apriltag(image, self.detector, self.tag_id)

            if results is None or self.goal_array is None or len(results) == 0:
                print("bot_"+str(self.tag_id)+"_stopped")
                self.stop()
            # if results is None:
                # print('No apriltag detected')
                # pass
            else:
                if len(results):
                    #xc, yc: x coordinates of center of bot
                    xc, yc = results[0].center

                    #front corner coordinates
                    x1, y1 = results[0].corners[1]
                    x2, y2 = results[0].corners[2]

                    #front mid coordinates
                    xm = (x1 + x2) / 2
                    ym = (y1 + y2) / 2

                    #xt, yt: coordinates of target point
                    #xi, yi: coordinates of initial point
                    xt, yt = self.goal_array[int(self.stage)]
                    xi, yi = self.goal_array[int(self.stage) - 1]

                    cv.arrowedLine(image, (int(xi), int(yi)), (int(xt), int(yt)), (255, 0, 0), 2)
                    cv.arrowedLine(image, (int(xc), int(yc)), (int(xt), int(yt)), (0, 0, 255), 2)
                    cv.arrowedLine(image, (int(xc), int(yc)), (int(xm), int(ym)), (0, 255, 0), 2)

                    error, euclidean_dist, abs_angle_diff = error_calculation(yi, yt, xt, xi, yc, ym, xc, xm)

                    #maneuver function
                    if self.dropped == False:
                        self.FollowStraight(euclidean_dist, error, self.params['SP'])
                    else:
                        self.Rotate(error, abs_angle_diff)

                    #DhoomOP :-)
                    cv.imshow("fast_n_furious_{}".format(self.tag_id), image)

                    #msg publish
                    self.pub_twist.publish(self.msg_twist)

            if cv.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown()
        except CvBridgeError as e:
            print(e)

    def execute_cb(self, goal):
        self.success = False
        self.goal_array = [(goal.order[0],goal.order[1]), (goal.order[2], goal.order[3])]
        print('Incoming Goal ', self.goal_array, ' Previous Goal ', self.prev_goal)

        if len(goal.order)==5:
            self.dropped = True

        while True:
            if self.success is False:
                continue
            else:
                break

        if self.success:
            self.prev_goal = self.goal_array
            self.goal_array = None
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
        else:
            rospy.loginfo("dekh")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tag_id", nargs="?", type=int, default=1)

    args = parser.parse_args()

    try:
        rospy.init_node('bot_maneuver_{}'.format(args.tag_id))
        result = BotManeuver('botAction', args)
    except rospy.ROSInterruptException:
        pass
