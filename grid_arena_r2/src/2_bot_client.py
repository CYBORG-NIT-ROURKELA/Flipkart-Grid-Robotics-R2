#! /usr/bin/env python

from destination import give_destination
from schedule import find_schedule2
from centroids import findCoordinates, findDiscreteCoordinates, RealToDiscrete, findRealCoordinates
from grid_arena_r2.msg import botAction, botGoal
import actionlib
import rospy
import time
import csv
import numpy as np

bot_color1 = (0,255,0)
bot_color2 = (0,0,255)

def give_cities(file_path):
    file = open(file_path)
    csvreader = csv.reader(file)
    station1_cities = []
    station2_cities  = []
    for row in csvreader:
        if row[1]=='1':
            station1_cities.append(row)
        elif row[1] == '2':
            station2_cities.append(row)
    file.close()
    return station1_cities, station2_cities

def path_client():
    print('init client')

    initial1=dock2 = [0,4]
    initial2=dock1 = [0,9]
    m=n=0
    station2,station1 = give_destination('Sample Data - Sheet1.csv')
    agent1_dropped = 0
    agent2_dropped = 0
    city1,city2 = give_cities('Sample Data - Sheet1.csv')

    agent1_dest = station1[0][2]
    agent2_dest = station2[0][2]

    while m<len(station1) and n<len(station2):
        if type(initial1) == dict:
            initial1 = findDiscreteCoordinates(initial1)
            initial2 = findDiscreteCoordinates(initial2)

        schedule = find_schedule2(initial1 , agent1_dest ,initial2, agent2_dest )
        # blank_image = np.zeros((300,800,3), np.uint8)
        # cv.putText(blank_image, "package "+ city1[m][0]+" bot 1 to "+city1[m][2], (30,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv.LINE_AA)
        # cv.putText(blank_image, "package "+ city2[n][0]+" bot 2 to "+city2[n][2], (30,200), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv.LINE_AA)
        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")

        print("package "+ city1[m][0]+" bot 1 to "+city1[m][2])
        print("package "+ city2[n][0]+" bot 2 to "+city2[n][2])

        agent1_end = agent1_rc[-1]
        agent2_end = agent2_rc[-1]


        agent1_state = agent1_rc[0]
        agent2_state = agent2_rc[0]
        # time.sleep(1.5)
        agent1_state,agent2_state,agent1_dropped,agent2_dropped = complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped)
        print("Number of packages delivered : ", m+n+1)
        initial1,agent1_dest,m,agent1_dropped = where_to_where(agent1_dropped,agent1_state,dock2,agent1_dest,station1[m+1][2],m)
        initial2,agent2_dest,n,agent2_dropped = where_to_where(agent2_dropped,agent2_state,dock1,agent2_dest,station2[n+1][2],n)



def complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped):

    i=j=0
    len1 = len(agent1_rc)
    len2 = len(agent2_rc)

    client = actionlib.SimpleActionClient('botAction_1', botAction)
    client_2 = actionlib.SimpleActionClient('botAction_7', botAction)

    client.wait_for_server()
    print("client 1 connected")
    client_2.wait_for_server()
    print("client 1 connected")

    if len1>len2:
        len1+=1
    else:
        len2+=1
    while i<len1-1 and j<len2-1:
            goal_coords1 = [[agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]+2,agent1_state["x_c"],agent1_state["y_c"]+2]]
            goal_coords2 = [[agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]+2,agent2_state["x_c"],agent2_state["y_c"]+2]]


            print("client 1 moving from => "+str(RealToDiscrete([agent1_state["x_c"],agent1_state["y_c"]])) + " => "+ str(RealToDiscrete([agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]])))
            print("client 2 moving from => "+str(RealToDiscrete([agent2_state["x_c"],agent2_state["y_c"]])) + " => "+ str(RealToDiscrete([agent2_rc[i+1]["x_c"],agent2_rc[i+1]["y_c"]])))

            # Creates a goal to send to the action server.
            goal = botGoal(order=goal_coords1[0])
            goal2 = botGoal(order=goal_coords2[0])
            print('goals ready')

            # Sends the goal to the action server.
            client.send_goal(goal2)
            client_2.send_goal(goal)
            # Waiting for the bot to complete their respective goals
            client.wait_for_result() and client_2.wait_for_result()
            print('result received')
            
            if i<len1-1:
                i+=1
            if j<len2-1:
                j+=1
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]
            if findDiscreteCoordinates(agent1_state) == [0,4]:
                print("agent1 dropped")
                agent1_dropped = 2
            elif agent1_state == agent1_end:
                agent1_dropped = 1
                print("agent1 reached")
                rotated_cord = rotate_to_drop(agent1_state)
                goal1 = [[rotated_cord[0], rotated_cord[1], agent1_state['x_c'], agent1_state['y_c'], 1]]
                goal = botGoal(order = goal1[0])
                client_2.send_goal(goal)
                print("client 1 delivering")
                client_2.wait_for_result()

            if findDiscreteCoordinates(agent2_state) == [0,9]:
                print("agent2 dropped")
                agent2_dropped = 2
            elif agent2_state == agent2_end:
                agent2_dropped = 1
                print("agent2 reached")
                rotated_cord = rotate_to_drop(agent2_state)
                goal2 = [[rotated_cord[0], rotated_cord[1], agent2_state['x_c'], agent2_state['y_c'], 1]]
                goal = botGoal(order = goal2[0])
                client.send_goal(goal)
                print("client 2 delivering")
                client.wait_for_result()

    return agent1_rc[i],agent2_rc[j],agent1_dropped,agent2_dropped

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

def rotate_to_drop(coord):
    b = findDiscreteCoordinates(coord)
    if b[1]==1 or b[1]==5 or b[1]==9:
        b[1]+=1
    elif b[1]==4 or b[1]==8 or b[1]==12:
        b[1]-=1
    else:
        b[0]+=1
    rotated_coor = findRealCoordinates(b)
    return rotated_coor


if __name__ == '__main__':
    try:
        rospy.init_node('two_bot_client')
        path_client()
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
