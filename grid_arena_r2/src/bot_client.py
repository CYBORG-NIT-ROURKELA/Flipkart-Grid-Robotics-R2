
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

    # Creates a goal to send to the action server.
    goal2 = botGoal(order=[281, 504, 331, 504])
    goal = botGoal(order=[281, 265, 331, 265])

    print('goals ready')
    # Sends the goal to the action server.
    client.send_goal(goal)
    client_2.send_goal(goal2)

    print('goals sent')

    # Waits for the server to finish performing the action.
    client.wait_for_result()
    client_2.wait_for_result()

    print('result received')

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('fibonacci_client_py')
        result = fibonacci_client()
        # print("Result:", ', '.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
