#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import time
import numpy as np
from schedule import find_schedule
from centroids import findCoordinates
from destination import give_destination





# schedule = find_schedule([0,8],[11,4],[0,4],[8,9])
# agent0_path = findCoordinates(schedule,"agent0")
# agent1_path = findCoordinates(schedule,"agent1")


class Planned_path:

    def __init__(self):
        rospy.init_node('plan_path')
        self.sub = rospy.Subscriber('/head/image_raw', Image, self.callback)
        
        self.bridge = CvBridge()
        self.m = self.n = 0
        self.dock1 = [0,4]
        self.dock2 = [0,9]
        self.station1,self.station2 = give_destination('/home/adyasha/Desktop/Sample Data - Sheet1.csv')

        
        
        
    def callback(self, data):
        try:


            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            img = cv_image.copy()
            image = cv_image.copy()
            

            # while self.m<len(self.station1) and self.n<len(self.station2):
            while self.m<1 and self.n<1:
                
                i=0
                j=0
                agent1_dest = self.station1[self.m][2]
                agent2_dest = self.station2[self.n][2]
                print(self.dock1,agent1_dest,self.dock2,agent2_dest)
                print(self.m, self.n)
               
                

                schedule = find_schedule(self.dock1,agent1_dest,self.dock2,agent2_dest)
                
                agent1_rc = findCoordinates(schedule,"agent0")
                agent2_rc = findCoordinates(schedule,"agent1")
                
         

                agent1_state = agent1_rc[0]
                agent2_state = agent2_rc[0]

                len1 = len(agent1_rc)
                len2 = len(agent2_rc)
                len_1 = len1
                len_2 = len2
                if len1>len2:
                    len1+=1
                else:
                    len2+=1
                # while (i<len1-2) or (j<len2-2):
                   
                #     print(i,j)
                #     cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]),
                #                             (0,255,0), 4)
                #     print(i, agent1_state["x_c"],agent1_state["y_c"]), (agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"])
                #     cv.arrowedLine(image, (agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]),
                #                             (255,0,0), 4)
                #     print(j, agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"])
                    
                #     if i<len1-2:
                #         i+=1
                #     if j<len2-2:
                #         j+=1
        
                    
                #     agent1_state = agent1_rc[i]
                #     agent2_state =  agent2_rc[j]
                    
                    # cv.imshow('image', image)
                    # cv.imshow('img', img)
                
                i = len_1-1
                j = len_2-1
                if j>i:
                    lower_j = 0
                    lower_i=1
                else:
                    lower_j=1
                    lower_i = 0
                
                agent1_state = agent1_rc[i]
                agent2_state =  agent2_rc[j]
                while i>lower_i or j>lower_j:
                    print(i,j)
                    cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_rc[i-1]["x_c"],agent1_rc[i-1]["y_c"]),
                                            (0,255,0), 4)
                    cv.arrowedLine(image, (agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j-1]["x_c"],agent2_rc[j-1]["y_c"]),
                                            (255,0,0), 4)
                    # maneuver(agent1_state,agent1_rc[i-1],agent2_state,agent2_rc[j-1])
                    if i>lower_i:
                        i-=1
                    if j>lower_j:
                        j-=1
                    agent1_state = agent1_rc[i]
                    agent2_state = agent2_rc[j]
                
                

                self.m+=1
                self.n+=1


            cv.imshow('image', image)
            cv.imshow('img', img)

               
                

                



   
   
           

            
            
            # dest1 = station1[self.m]
            # dest2 = station2[self.n]

            # agent1_p
            # # start1 = dock1
            # # start2 = dock2

            # while(self.m<141 and self.n<141):
            #     i=j=0
            #     goal1 = dest1[2]

            #     goal2 = dest2[2]
            #     schedule = find_schedule(start1,goal1,start2,goal2)
            #     agent0_path = findCoordinates(schedule,"agent0")
            #     agent1_path = findCoordinates(schedule,"agent1")


            
            #     i_end = len(agent0_path)-1
            #     j_end = len(agent1_path)-1

            #     agent0_last = agent0_path[len(agent0_path)-1]
            #     agent1_last = agent1_path[len(agent1_path)-1]
            #     agent0_state = agent0_path[i]
            #     agent1_state = agent1_path[j]
                
            


            #     while agent0_state!=agent0_last or agent1_state!=agent1_last:
            #         if i!=i_end:
                        
            #             image = cv.arrowedLine(image, (agent0_state["x_c"],agent0_state["y_c"]), (agent0_path[i+1]["x_c"],agent0_path[i+1]["y_c"]),
            #                                 (0,255,0), 4)
                        

            #         if j!=j_end:

            #             image = cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_path[j+1]["x_c"],agent1_path[j+1]["y_c"]),
            #                                 (0,0,255), 4)
                        

            #         if i!=i_end:
            #             i+=1
            #         if j!=j_end:
            #             j+=1
            #         agent0_state = agent0_path[i]
            #         agent1_state = agent1_path[j]
            #     self.m+=1
            #     self.n+=1
                        
            #     crop_image = image[112:654, 287:909]
                
                # cv.imshow('cropped',crop_image)

        except CvBridgeError as e:
            print(e)

        if cv.waitKey()==27:                    # ESC to end program
            rospy.signal_shutdown("shutdown")
            cv.destroyAllWindows()

        # k = cv.waitKey(0) & 0xFF 
       
       

if __name__ == '__main__':
    pps = Planned_path()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
