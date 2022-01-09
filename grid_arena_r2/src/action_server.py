#! /usr/bin/env python

import rospy
import actionlib
from grid_arena_r2.msg import botAction, botFeedback, botResult
import argparse
import apriltag
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np
import math
import sys

from utils import detect_apriltag, error_calculation

from dynamic_reconfigure.server import Server
# from grid_arena.cfg import pidConfig

class BotManeuver:
    _feedback = botFeedback()
    _result = botResult()

    def __init__(self, name, args):
        self._action_name = str(name)+"_"+str(args.tag_id)
        print(self._action_name)

        if args.tag_id == 0:
            self.pub_twist = rospy.Publisher('grid_robot/cmd_vel', Twist, queue_size=10)
        else:
            self.pub_twist = rospy.Publisher('grid_robot_{}/bot{}/cmd_vel'.format(args.tag_id,args.tag_id), Twist, queue_size=10)
        

        #self.rate = rospy.Rate(100)
        self.msg_twist = Twist()
        self.bridge = CvBridge()

        self.stage = 0
        self.tag_id = args.tag_id
        print(self.tag_id)
        # self.thresh_dist = 30
        self.goal_array = None
        self.prev_goal = None
        self.image = None

        self.intg, self.last_error = 0.0, 0.0
        # self.rate.sleep()
        self.params = {'KP': 0.04, 'KD': 0.2, 'KI': 0, 'SP': 0.27}

        self._as = actionlib.SimpleActionServer(self._action_name, botAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        print('action server {} started'.format(args.tag_id))

        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
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

    def FollowStraight(self, xt, xc, euclidean_dist, angle_target, cross_track_error, error, linear_vel):
        if euclidean_dist > 15 or euclidean_dist < -15:
            ang_vel = 0

            if 1.05 < angle_target <= 1.57:
                ang_vel = self.pid(-cross_track_error, self.params)
            elif 1.57 < angle_target < 2.09:
                ang_vel = self.pid(cross_track_error, self.params)

            elif -2.09 < angle_target <= -1.57:
                ang_vel = self.pid(cross_track_error, self.params)
            elif -1.57 < angle_target < -1.05:
                ang_vel = self.pid(-cross_track_error, self.params)

            elif -0.523 < angle_target < 0.523:
                ang_vel = self.pid(-cross_track_error, self.params)

            elif -3.15 < angle_target < -2.617:
                ang_vel = self.pid(-cross_track_error, self.params)
            elif 2.617 < angle_target < 3.15:
                ang_vel = self.pid(cross_track_error, self.params)
            
            self.msg_twist.linear.x = linear_vel
            self.msg_twist.angular.z = ang_vel

        else:
            self.stop()
            print("reached target coordinate")
            self.success = True


    def Rotate(self, error, abs_angle_diff):
        if abs_angle_diff > 0.1:
            if error > 3.14:
                ang_vel = self.pid(25*(error-6.28), self.params)
            elif error < -3.14:
                ang_vel = self.pid(25*(error+6.28), self.params)
            else:
                ang_vel = self.pid(25*error, self.params)
            self.msg_twist.angular.z = ang_vel

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
        if abs_angle_diff > 0.1:
            self.Rotate(error, abs_angle_diff)
        else:
            self.FollowStraight(xt, xc, euclidean_dist, angle_target, cross_track_error, error, 0.18)

    def callback(self, data):
        try:
            #recieving image
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            #detecting apriltag
            results = detect_apriltag(image, self.tag_id)
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

                    cv.arrowedLine(image, (int(xi), int(yi)), (int(xt), int(yt)), (255, 0, 0), 2)
                    cv.arrowedLine(image, (int(xc), int(yc)), (int(xm), int(ym)), (0, 255, 0), 2)

                    abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error = error_calculation(yi, yt, xt, xi, yc, ym, xc, xm)

                    self.maneuver(xt, xc, abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error)

                    cv.imshow("fast_n_furious_{}".format(self.tag_id), image)

                    self.pub_twist.publish(self.msg_twist)

            if cv.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown()
        except CvBridgeError as e:
            print(e)

    def execute_cb(self, goal):
        self.success = False
        r = rospy.Rate(1)
        self.goal_array = [(goal.order[0],goal.order[1]), (goal.order[2], goal.order[3])]
        print('Incoming Goal ', self.goal_array, ' Previous Goal ', self.prev_goal)
        # if self.goal_array == self.prev_goal:
        #     self.success = True

        # append the seeds for the fibonacci sequence
        # self._feedback.sequence = []
        # self._feedback.sequence.append(0)
        # self._feedback.sequence.append(1)

        # publish info to the console for the user
        # rospy.loginfo('%s: Executing, creating fibonacci sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))

        while True:
            if self.success is False:
                continue
            else:
                break

        # start executing the action
        # for i in range(1, goal.order):
        #     # check that preempt has not been requested by the client
        #     if self._as.is_preempt_requested():
        #         rospy.loginfo('%s: Preempted' % self._action_name)
        #         self._as.set_preempted()
        #         success = False
        #         break
        #     self._feedback.sequence.append(self._feedback.sequence[i] + self._feedback.sequence[i-1])
        #     # publish the feedback
        #     self._as.publish_feedback(self._feedback)
        #     # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
        #     r.sleep()

        if self.success:
            # self._result.sequence = self._feedback.sequence
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
        print("program interrupted before completion")
