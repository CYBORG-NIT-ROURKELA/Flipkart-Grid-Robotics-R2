import cv2 as cv
import apriltag
import math
import numpy as np


def detect_apriltag(image, detector, id):
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    results = detector.detect(imgray)
    for result in results:
        if result.tag_id == id:
            return [result]


def error_calculation(yi, yt, xt, xi, yc, ym, xc, xm):
    angle_target = math.atan2((yc-yt), (xt - xc))

    angle_bot = math.atan2((yc-ym),(xm-xc))

    m = math.tan(angle_target)

    euclidean_dist = np.linalg.norm(np.array([xc, yc]) - np.array([xt, yt]))

    cross_track_error = (m*xc-yc+yi-m*xi)/(m**2+1)**0.5
    angle_orientation_factor = (m*xm-ym+yc-m*xc)/(m**2+1)**0.5

    abs_angle_diff = abs(angle_target - angle_bot)
    error = angle_target-angle_bot

    return abs_angle_diff, error, euclidean_dist, angle_target, cross_track_error
