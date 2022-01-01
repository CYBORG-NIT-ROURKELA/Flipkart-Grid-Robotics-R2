#! /usr/bin/env python3

from __future__ import print_function
import rospy


# Brings in the SimpleActionClient
import actionlib
from grid_arena_r2.msg import botAction, botGoal
from schedule import find_schedule
from centroids import findCoordinates
from destination import give_destination, param

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.

def find_dest(schedule):
    a1 = schedule['schedule']['agent0']
    a2 = schedule['schedule']['agent1']

    initial1 = [a1[0]['x'], a1[0]['y']]
    final1 = [a1[-1]['x'], a1[-1]['y']]

    initial2 = [a2[0]['x'], a2[0]['y']]
    final2 = [a2[-1]['x'], a2[-1]['y']]

    for key in param['1']:
        if param['1'][key] == initial1:
            print("starting point for bot 1 ", key)

    for key in param['1']:
        if param['1'][key] == final1:
            print("final point for bot 1 ", key)

    for key in param['2']:
        if param['2'][key] == initial2:
            print("starting point for bot 2 ", key)

    for key in param['2']:
        if param['2'][key] == final2:
            print("final point for bot 2 ", key)

def fibonacci_client():
    print('init client')
    dock2 = [0,4]
    dock1 = [0,9]
    m=n=0
    station1,station2 = give_destination('Sample Data - Sheet1.csv')
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('botAction_0', botAction)
    client_2 = actionlib.SimpleActionClient('botAction_1', botAction)
    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    client_2.wait_for_server()

    print('server active')
    while m<len(station1) and n<len(station2):
        i=j=0
        agent1_dest = station1[m][2]
        agent2_dest = station2[n][2]
        print(dock1,agent1_dest,dock2,agent2_dest)
        print(m, n)
        schedule = find_schedule(dock1,agent1_dest,dock2,agent2_dest)
        find_dest(schedule)
        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")

        agent1_state = agent1_rc[i]
        agent2_state = agent2_rc[j]
        len1 = len(agent1_rc)
        len2 = len(agent2_rc)
        len_1 = len1
        len_2 = len2
        if len1>len2:
            len1+=1
        else:
            len2+=1
        while i<len1-2 or j<len2-2:
            goal_coords2 = [[agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"],agent1_state["x_c"],agent1_state["y_c"]]]
            goal_coords1 = [[agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"],agent2_state["x_c"],agent2_state["y_c"]]]

            # Creates a goal to send to the action server.
            goal = botGoal(order=goal_coords1[0])
            goal2 = botGoal(order=goal_coords2[0])
            print('goals ready')
            # Sends the goal to the action server.
            client.send_goal(goal2)
            client_2.send_goal(goal)

            print('goals sent')
            # Waits for the server to finish performing the action.
            # client.wait_for_result()
            client.wait_for_result() and client_2.wait_for_result()

            print('result received')
            if i<len1-2:
                i+=1
            if j<len2-2:
                j+=1
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]
        i = len_1-1
        j = len_2-1
        if j>i:
            lower_i = 1
            lower_j = 0
        else:
            lower_i = 0
            lower_j = 1
        agent1_state = agent1_rc[i]
        agent2_state =  agent2_rc[j]
        print("Mission delivery complete")
        while i>lower_i or j>lower_j:
            goal_coords2 = [[agent1_rc[i-1]["x_c"],agent1_rc[i-1]["y_c"],agent1_state["x_c"],agent1_state["y_c"]]]
            goal_coords1 = [[agent2_rc[j-1]["x_c"],agent2_rc[j-1]["y_c"],agent2_state["x_c"],agent2_state["y_c"]]]

            # Creates a goal to send to the action server.
            goal = botGoal(order=goal_coords1[0])

            goal2 = botGoal(order=goal_coords2[0])
            print('goals ready')
            # Sends the goal to the action server.
            client.send_goal(goal2)
            client_2.send_goal(goal)

            print('goals sent')

            # Waits for the server to finish performing the action.
            # client.wait_for_result()
            client.wait_for_result() and client_2.wait_for_result()

            print('result received')
            if i>lower_i:
                i-=1
            if j>lower_j:
                j-=1
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]
        print("Mission back 2 home complete")
        m+=1
        n+=1




    # goal_coords1 = [[234, 314, 234, 264]]
    # goal_coords1 = [[284,264,234,264], [284, 314, 284, 264]]

    # Prints out the result of executing the action
    # print(client.get_result())
    # return client.get_result()  # A FibonacciResult


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('fibonacci_client_py')
        fibonacci_client()
        # print("Result:", ', '.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
