#!/usr/bin/env python

import argparse
import socket
import telnetlib
import rospy
from geometry_msgs.msg import Twist
import math
from grid_arena_r2.msg import rpm
from std_msgs.msg import Int64


class Transmitter:
    def __init__(self, args):
        rospy.init_node('transmitter_{}'.format(args.topic_number))
        rospy.Subscriber('grid_robot_{}/cmd_vel'.format(args.topic_number), Twist, self.callback_twist)
        rospy.Subscriber('grid_robot_{}/servo_angle'.format(args.topic_number), Int64, self.callback_servo)

        self.ip = args.ip
        self.port = args.port
        self.is_telnet = args.telnet

        if self.is_telnet:
            self.telnet = telnetlib.Telnet(args.ip, args.port)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        rospy.loginfo("Connected to %s:%s", args.ip, args.port)

        self.left_rpm = 0
        self.right_rpm = 0
        self.servo_angle = 0

    def callback_twist(self, data):
        v1 = data.linear.x - (data.angular.z*0.0875)/2
        v2 = data.linear.x + (data.angular.z*0.0875)/2

        self.left_rpm = (30*v1)/(math.pi*0.03459)
        self.right_rpm = (30*v2)/(math.pi*0.03459)
        self.transmit()

    def rpm2pwm(self, rpm):
        return rpm * 1024 / 138

    def callback_servo(self, data):
        self.servo_angle = data.data
        self.transmit()

    def transmit(self):
        msg = "{},{},{}\r".format(self.rpm2pwm(self.left_rpm),
                                  self.rpm2pwm(self.right_rpm),
                                  self.servo_angle)
        print(msg)
        if self.is_telnet:
            self.telnet.write(msg.encode('ascii'))
        else:
            self.sock.sendto(str.encode(msg), (self.ip, self.port))
            # print(self.sock.recv())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', nargs='?', type=str, help='ip address')
    parser.add_argument('--port', type=int, default=4210,
                        help='port, default: 4210')
    parser.add_argument('-t', '--topic_number', type=int, default=0,
                        help='motor rpm topic number, default: 0')
    parser.add_argument('--telnet', action='store_true', help='use telnet flag')
    args = parser.parse_args()

    print("host: %s, port: %s", args.ip, args.port)

    tm = Transmitter(args)
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
