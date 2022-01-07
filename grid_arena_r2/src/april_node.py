#! /usr/bin/env python
import rospy
import apriltag
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

class ApriltagDetect:
    def __init__(self):
        rospy.init_node('apriltag_detect')
        self.sub = rospy.Subscriber('grid_robot/image_feed', Image, self.callback)
        self.detector = apriltag.Detector()
        self.bridge = CvBridge()

    def callback(self, data):
        image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        results = self.detector.detect(gray)

        if len(results):
            for r in results:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
                (ptA, ptB, ptC, ptD) = r.corners
                ptB = (int(ptB[0]), int(ptB[1]))
                ptC = (int(ptC[0]), int(ptC[1]))
                ptD = (int(ptD[0]), int(ptD[1]))
                ptA = (int(ptA[0]), int(ptA[1]))
                # draw the bounding box of the AprilTag detection
                cv2.line(image, ptA, ptB, (0, 255, 0), 2)
                cv2.line(image, ptB, ptC, (0, 255, 0), 2)
                cv2.line(image, ptC, ptD, (0, 255, 0), 2)
                cv2.line(image, ptD, ptA, (0, 255, 0), 2)
                # draw the center (x, y)-coordinates of the AprilTag
                (cX, cY) = (int(r.center[0]), int(r.center[1]))
                cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
                # draw the tag family on the image
                tagFamily = r.tag_family.decode("utf-8")
                cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("frame", image)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()

if __name__ == '__main__':
    ad = ApriltagDetect()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)