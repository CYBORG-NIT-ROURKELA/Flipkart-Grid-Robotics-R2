#! /usr/bin/env python

from destination import give_destination
from schedule import find_schedule2
from centroids import findCoordinates, findDiscreteCoordinates, RealToDiscrete
from grid_arena_r2.msg import botAction, botGoal
import actionlib
import rospy
# import time

import cv2 as cv

bot_color1 = (0,255,0)
bot_color2 = (0,0,255)

# cap = cv.VideoCapture(2)
def fibonacci_client():
    print('init client')

    
    
    initial1=dock2 = [0,4]
    initial2=dock1 = [0,9]
    m=n=0
    station2,station1 = give_destination('/home/adyasha/flipkart_ws/src/Flipkart-Grid-Robotics-R2/grid_arena_r2/src/Sample Data - Sheet1.csv')
    agent1_dropped = 0
    agent2_dropped = 0

    
    agent1_dest = station1[0][2]
    agent2_dest = station2[0][2]

    while m<len(station1) and n<len(station2):
        # print(initial1 , agent1_dest ,initial2, agent2_dest )
        if type(initial1) == dict:
            initial1 = findDiscreteCoordinates(initial1)
            initial2 = findDiscreteCoordinates(initial2)
        
        schedule = find_schedule2(initial1 , agent1_dest ,initial2, agent2_dest )

        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")
        # print(schedule)
        # print("agent1rc",agent1_rc)
        # print("agent2rc",agent2_rc)
        # for element in agent1_rc:
        #     print(element)
        #     print(findDiscreteCoordinates(element))
        # exit()
    
        
        
        agent1_end = agent1_rc[-1]
        agent2_end = agent2_rc[-1]


        agent1_state = agent1_rc[0]
        agent2_state = agent2_rc[0]

        agent1_state,agent2_state,agent1_dropped,agent2_dropped = complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped)
        # print("before", findDiscreteCoordinates(agent1_state),findDiscreteCoordinates(agent2_state))
        initial1,agent1_dest,m,agent1_dropped = where_to_where(agent1_dropped,agent1_state,dock2,agent1_dest,station1[m+1][2],m)
        initial2,agent2_dest,n,agent2_dropped = where_to_where(agent2_dropped,agent2_state,dock1,agent2_dest,station2[n+1][2],n)
        # print("after ", findDiscreteCoordinates(initial1), agent1_dest,findDiscreteCoordinates(initial2), agent2_dest)

        
       
def complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped):
    # print('complete_iter entered')
    # print('Verifying Goal Coordinates for agent1')
    
    i=j=0
    len1 = len(agent1_rc)
    len2 = len(agent2_rc)

    client = actionlib.SimpleActionClient('botAction_1', botAction)
    client_2 = actionlib.SimpleActionClient('botAction_2', botAction)

    client.wait_for_server()
    print("client 1 connected")
    client_2.wait_for_server()
    print("client 1 connected")

    if len1>len2:
        len1+=1
    else:
        len2+=1
    while i<len1-1 and j<len2-1:
            goal_coords1 = [[agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"],agent1_state["x_c"],agent1_state["y_c"]]]
            goal_coords2 = [[agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"],agent2_state["x_c"],agent2_state["y_c"]]]

            #visualisation
            # _, image = cap.read()
            # cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]), bot_color1, 2)
            # cv.arrowedLine(image, (agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]), bot_color2, 2)
            # print(goal_coords1, i, j)

            print("client 1 moving from => "+str(RealToDiscrete([agent1_state["x_c"],agent1_state["y_c"]])) + " => "+ str(RealToDiscrete([agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]])))
            print("client 2 moving from => "+str(RealToDiscrete([agent2_state["x_c"],agent2_state["y_c"]])) + " => "+ str(RealToDiscrete([agent2_rc[i+1]["x_c"],agent2_rc[i+1]["y_c"]])))

            # Creates a goal to send to the action server.
            goal = botGoal(order=goal_coords1[0])
            goal2 = botGoal(order=goal_coords2[0])
            print('goals ready')
            # Sends the goal to the action server.
            client.send_goal(goal2)
            client_2.send_goal(goal)

            # print('goals sent')
            # # Waits for the server to finish performing the action.
            # # client.wait_for_result()
            client.wait_for_result() and client_2.wait_for_result()
            # cv.imshow("image", image)
            # if cv.waitKey(1) == 27:
            #     cv.destroyAllWindows()
            #     break

            print('result received')
            if i<len1-1:
                i+=1
            if j<len2-1:
                j+=1
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]
            if agent1_state["x_c"] == 51 and agent1_state["y_c"]==312:
                print("agent1 dropped")
                agent1_dropped = 2
            elif agent1_state == agent1_end:
                agent1_dropped = 1
                print("agent1 reached")

            if agent2_state["x_c"] == 51 and agent2_state["y_c"]==127 :
                print("agent2 dropped")
                agent2_dropped = 2
            elif agent2_state == agent2_end:
                agent2_dropped = 1
                print("agent2 reached")

            

    return agent1_rc[i],agent2_rc[j],agent1_dropped,agent2_dropped
    # return agent1_state,agent2_state,agent1_dropped,agent2_dropped


def where_to_where(dropped,current ,dock,dest,next_dest,iter):
    if dropped == 0:
        initial = current
        final = dest
    elif dropped == 1:
        initial = current
        final = dock
    else:
        iter+= 1
        dropped = 0
        initial = current
        final = next_dest
    return initial,final,iter,dropped


    

if __name__ == '__main__':
    try:
        rospy.init_node('fibonacci_client_py')
        fibonacci_client()
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
