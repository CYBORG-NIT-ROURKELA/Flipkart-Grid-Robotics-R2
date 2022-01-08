#! /usr/bin/env python

from destination import give_destination
from schedule import find_schedule2
from centroids import findCoordinates, findDiscreteCoordinates, findRealCoordinates
import cv2

bot1_color = (255,0,0)
bot2_color = (0,255,0)

def fibonacci_client():
    print('init client')
    initial1=dock2 = [0,4]
    initial2=dock1 = [0,9]
    m=n=0
    station2,station1 = give_destination('Sample Data - Sheet1.csv')
    agent1_dropped = 0
    agent2_dropped = 0

    agent1_state = [285,176]
    agent2_state =  [296,300]
    agent1_dest = station1[0][2]
    agent2_dest = station2[0][2]

    while m<len(station1) and n<len(station2):
        image = cv2.imread('image1.png')
        if type(initial1) == dict:
            initial1 = findDiscreteCoordinates(initial1)
            initial2 = findDiscreteCoordinates(initial2)
        
        cv2.drawMarker(image, tuple(findRealCoordinates(agent2_dest)), bot2_color,1,10,3)
        cv2.drawMarker(image, tuple(findRealCoordinates(agent1_dest)), bot1_color,1,10,3)

        print(agent1_dest, agent2_dest)

        schedule = find_schedule2(initial1 , agent1_dest ,initial2, agent2_dest)
        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")
        
        agent1_end = agent1_rc[-1]
        agent2_end = agent2_rc[-1]

        agent1_state = agent1_rc[0]
        agent2_state = agent2_rc[0]

        agent1_state,agent2_state,agent1_dropped,agent2_dropped = complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped, image)
        initial1,agent1_dest,m,agent1_dropped = where_to_where(agent1_dropped,agent1_state,dock2,agent1_dest,station1[m+1][2],m)
        initial2,agent2_dest,n,agent2_dropped = where_to_where(agent2_dropped,agent2_state,dock1,agent2_dest,station2[n+1][2],n)
    cv2.destroyAllWindows()

        
       
def complete_iter(agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped, image):
    # print('Verifying Goal Coordinates for agent1')
    # for element in agent1_rc:
    #     print(findDiscreteCoordinates(element))
    # print('Verifying Goal Coordinates for agent2')
    # for element in agent2_rc:
    #     print(findDiscreteCoordinates(element))
    i=j=0
    len1 = len(agent1_rc)
    len2 = len(agent2_rc)

    
    # if len1>len2:
    #     len1+=1
    # else:
    #     len2+=1
    # print(len1,len2)
    while i<len1-1 and j<len2-1:
            goal_coords1 = [[agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"],agent1_state["x_c"],agent1_state["y_c"]]]
            goal_coords2 = [[agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"],agent2_state["x_c"],agent2_state["y_c"]]]
            
            cv2.arrowedLine(image, (agent1_state["x_c"]+3,agent1_state["y_c"]+4), (agent1_rc[i+1]["x_c"]+3,agent1_rc[i+1]["y_c"]+4), bot1_color, 2)
            cv2.arrowedLine(image, (agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]), bot2_color, 2)

            if i<len1-1:
                i+=1
            if j<len2-1:
                j+=1
            # location has been changed
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]

            if agent1_state["x_c"] == 225 and agent1_state["y_c"]==506 :
                agent1_dropped = 2
            elif agent1_state == agent1_end:
                _, image = rotate_to_drop_vis(agent1_state.copy(), image)
                #rotate_to_drop(agent1_state)
                agent1_dropped = 1
            if agent2_state["x_c"] == 225 and agent2_state["y_c"]==268 :
                agent2_dropped = 2
            elif agent2_state == agent2_end:
                _, image = rotate_to_drop_vis(agent2_state.copy(), image)
                #rotate_to_drop(agent2_state)
                agent2_dropped = 1
            
            cv2.imshow("image2", image)
            if cv2.waitKey(800) == 27:
                cv2.destroyAllWindows()
                break

            

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
    return findCoordinates(b)

def rotate_to_drop_vis(coord, image):
    b = findDiscreteCoordinates(coord)
    print('asila1')
    if b[1]==1 or b[1]==5 or b[1]==9:
        b[1]+=1
    elif b[1]==4 or b[1]==8 or b[1]==12:
        b[1]-=1
    else:
        b[0]+=1
    print('asila2')
    print(b)
    rotated_coor = findRealCoordinates(b)
    print('asila3')
    cv2.arrowedLine(image, (coord["x_c"],coord["y_c"]), tuple(rotated_coor), (127,127,100), 2)
    print('asila4')
    return rotated_coor, image






    

if __name__ == '__main__':
    try:
        # rospy.init_node('fibonacci_client_py')
       
       
        fibonacci_client()
    except:
        pass
