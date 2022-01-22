#! /usr/bin/env python

from destination import give_destination, param, alt_param
from schedule import find_schedule
from centroids import findCoordinates, findDiscreteCoordinates, findRealCoordinates, RealToDiscrete
from grid_arena_r2.msg import botAction, botGoal
import actionlib
import rospy
import time
import cv2

dock1 = [0,9]
dock2 = [0,4]
dock1_alt = [1,13] #2
dock2_alt = [1,0] #3

bot1_color = (255,0,0)
bot2_color = (0,255,0)
bot3_color = (0,0,255)
bot4_color = (125,25,205)

bot_stats = {
    0: {
        'inducting_station': dock1,
        'current_pos': [0,9],
        'final_dest': None,
        'mission_status': 'Delivery'
    },
    1: {
        'inducting_station': dock2,
        'current_pos': [0,4],
        'final_dest': None,
        'mission_status': 'Delivery'
    },
    2: {
        'inducting_station': dock1,
        'current_pos': [14,9],
        'final_dest': None,
        'mission_status': 'Back To Home'
    },
    3: {
        'inducting_station': dock2,
        'current_pos': [14,4],
        'final_dest': None,
        'mission_status': 'Back To Home'
    }
}


def fibonacci_client():
    m, n = 1, 1
    station1,station2 = give_destination('/home/kamaljeet/cyborg_ws/src/Flipkart-Grid-Robotics-R2/grid_arena_r2/src/Sample Data - Sheet1.csv')

    while(m<len(station1) and n<len(station2)):
        # visualize stations
        image = cv2.imread('image1.png')
        # time.sleep(1)
        # image = cv2.circle(image, tuple(findRealCoordinates(station1[m][2])), 5, (0,0,255), -1)
        # image = cv2.circle(image, tuple(findRealCoordinates(station2[n][2])), 5, (255,0,0), -1)
        # cv2.imshow('image', image)
        # m+=1
        # n+=1
        # if cv2.waitKey(1)==27:                    # ESC to end program
        #     cv2.destroyAllWindows()

        initial1 = bot_stats[0]['current_pos']
        if bot_stats[0]['final_dest'] is not None:
            final1 = bot_stats[0]['final_dest']
        else:
            final1 = station1[m][2]
            bot_stats[0]['final_dest'] = final1
            m+=1
        
        initial2 = bot_stats[1]['current_pos']
        if bot_stats[1]['final_dest'] is not None:
            final2 = bot_stats[1]['final_dest']
        else:
            final2 = station2[n][2]
            bot_stats[1]['final_dest'] = final2
            n+=1
        
        initial3 = bot_stats[2]['current_pos']
        if bot_stats[2]['final_dest'] is not None:
            final3 = bot_stats[2]['final_dest']
        else:
            final3 = station1[m][2]
            bot_stats[2] = final2
            m+=1
        
        initial4 = bot_stats[3]['current_pos']
        if bot_stats[3]['final_dest'] is not None:
            final4 = bot_stats[3]['final_dest']
        else:
            final4 = station1[n][2]
            bot_stats[3] = final4
            n+=1
        
        print(final1, final2, final3, final4)
        
        if final1 == final3:
            final3 = dock1_alt
            bot_stats[2]['final_dest'] = final3
            m-=1
        if final2 == final4:
            final4 = dock2_alt
            bot_stats[3]['final_dest'] = final4
            n-=1
        
        if any([final1==final2, final2==final3, final3==final4, final4==final1]):
            final1, final2, final3, final4 = fix_same_dest(final1, final2, final3, final4)
            print("equal destination appeared")
            print(final1, final2, final3, final4)

        
        print('Finding Schedule')
        schedule = find_schedule(initial1 , final1 ,initial2, final2, initial3, final3, initial4, final4)


        agent1_rc = findCoordinates(schedule, 'agent0')
        agent2_rc = findCoordinates(schedule, 'agent1')
        agent3_rc = findCoordinates(schedule, 'agent2')
        agent4_rc = findCoordinates(schedule, 'agent3')

        move_bots(agent1_rc, agent2_rc, agent3_rc, agent4_rc, bot_stats, image)
        cv2.destroyAllWindows()
        break

    
    #cv2.destroyAllWindows()

def fix_same_dest(final1, final2, final3, final4):
    if final3 == final4:
        final3 = recieve_alt_dest(final3)
    

    return final1, final2, final3, final4

def recieve_alt_dest(dest):
    for key in param['1']:
        if param['1'][key] == dest:
            return alt_param[key+'_alt_alt']
        


def move_bots(agent1_rc, agent2_rc, agent3_rc, agent4_rc, bot_stats, image):
    i, j, k, l = 0, 0, 0, 0
    while i<(len(agent1_rc)-1) and j<(len(agent2_rc)-1) and k<(len(agent3_rc)-1) and l<(len(agent4_rc)-1):
        goal_coords1 = [[agent1_rc[i+1]["x_c"], agent1_rc[i+1]["y_c"], agent1_rc[i]["x_c"], agent1_rc[i]["y_c"]]]
        goal_coords2 = [[agent2_rc[j+1]["x_c"], agent2_rc[j+1]["y_c"], agent2_rc[j]["x_c"], agent2_rc[j]["y_c"]]]
        goal_coords3 = [[agent3_rc[k+1]["x_c"], agent3_rc[k+1]["y_c"], agent3_rc[k]["x_c"], agent3_rc[k]["y_c"]]]
        goal_coords4 = [[agent4_rc[l+1]["x_c"], agent4_rc[l+1]["y_c"], agent4_rc[l]["x_c"], agent4_rc[l]["y_c"]]]

        #visulisation section
        cv2.arrowedLine(image, (agent1_rc[i]["x_c"], agent1_rc[i]["y_c"]), (agent1_rc[i+1]["x_c"], agent1_rc[i+1]["y_c"]), bot1_color, 2)
        cv2.arrowedLine(image, (agent2_rc[j]["x_c"], agent2_rc[j]["y_c"]), (agent2_rc[j+1]["x_c"], agent2_rc[j+1]["y_c"]), bot2_color, 2)
        cv2.arrowedLine(image, (agent3_rc[k]["x_c"], agent3_rc[k]["y_c"]), (agent3_rc[k+1]["x_c"], agent3_rc[k+1]["y_c"]), bot3_color, 2)
        cv2.arrowedLine(image, (agent4_rc[l]["x_c"], agent4_rc[l]["y_c"]), (agent4_rc[l+1]["x_c"], agent4_rc[l+1]["y_c"]), bot4_color, 2)
        cv2.imshow("image", image)

        update_bot_stats(goal_coords1, goal_coords2, goal_coords3, goal_coords4)
        if cv2.waitKey(1000) == 27:
            cv2.destroyAllWindows()
            break

        i+=1
        j+=1
        k+=1
        l+=1
    
def check_for_equal_destinations(final1, final2, final3, final4):
    final = [final1, final2, final3, final4]
    d = {}
    for i in range(len(final)):
        if final[i] not in d:
            d[final[i]] = 1
        else:
            d[final[i]] += 1
    for key in d:
        if d[key] > 1:
            return True
    return False
def update_bot_stats(goal_coords1, goal_coords2, goal_coords3, goal_coords4):
    print(goal_coords1)
    print(process_goal_coords(goal_coords1))
    # bot_stats[0] = process_goal_coords(goal_coords1)
    # bot_stats[1] = process_goal_coords(goal_coords2)
    # bot_stats[2] = process_goal_coords(goal_coords3)
    # bot_stats[3] = process_goal_coords(goal_coords4)
    pass

def process_goal_coords(goal_coords):
    final = [goal_coords[0][0], goal_coords[0][1]]
    initial = [goal_coords[0][2], goal_coords[0][3]]
    return initial, final

def give_mission(m,n):
    pass

    

if __name__ == '__main__':
    try:
        # rospy.init_node('fibonacci_client_py')
        fibonacci_client()
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
