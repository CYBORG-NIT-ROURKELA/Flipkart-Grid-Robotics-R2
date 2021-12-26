#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import csv
import numpy as np
from schedule import find_schedule
from centroids import findCoordinates
from destination import give_destination


dock1 = [0,4]
dock2 = [0.9]
station1,station2 = give_destination('/home/adyasha/Desktop/Sample Data - Sheet1.csv')

i = j = 0

while i<len(station1) and j<len(station2):
    agent1_dest = station1[i][2]
    agent2_dest = station2[j][2]

    schedule = find_schedule(dock1,agent1_dest,dock2,agent2_dest)

    agent1_rc = findCoordinates(schedule,"agent0")
    agent2_rc = findCoordinates(schedule,"agent1")

    agent1_state = agent1_rc[0]
    agent2_state = agent2_rc[0]

    while agent1_state != agent1_rc
   