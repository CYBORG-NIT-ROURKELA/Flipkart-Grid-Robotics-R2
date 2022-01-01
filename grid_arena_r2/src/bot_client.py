
#! /usr/bin/env python3

from __future__ import print_function
import rospy


# Brings in the SimpleActionClient
import actionlib
from grid_arena_r2.msg import botAction, botGoal

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.

def fibonacci_client():
    print('init client')
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('botAction_0', botAction)
    client_2 = actionlib.SimpleActionClient('botAction_1', botAction)
    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    client_2.wait_for_server()

    print('server active')
    # goal_coords1 = [[234, 314, 234, 264]]
    # goal_coords1 = [[284,264,234,264], [284, 314, 284, 264]]
    goal_coords1 = [[284,264,234,264], [331,264,284,264], [384,264,331,264], [381,312,381,264]]
    goal_coords2 = [[278,501,228,501], [329,501,278,501], [384,501,329,501], [382,459,382,501]]

    i = 0
    j = 0
    while (i<len(goal_coords1) and j<len(goal_coords2)):

    # Creates a goal to send to the action server.
        goal = botGoal(order=goal_coords1[i])
        goal2 = botGoal(order=goal_coords2[j])
        print(i, "koun sa ggoal")
        print('goals ready')
        # Sends the goal to the action server.
        client.send_goal(goal)
        client_2.send_goal(goal2)

        print('goals sent')

        # Waits for the server to finish performing the action.
        # client.wait_for_result()
        client.wait_for_result() and client_2.wait_for_result()

        print('result received')
        i+=1
        j+=1

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