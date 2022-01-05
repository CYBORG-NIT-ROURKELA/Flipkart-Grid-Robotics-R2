#! /usr/bin/env python

from destination import give_destination
from schedule import find_schedule
from centroids import findCoordinates, findDiscreteCoordinates
from grid_arena_r2.msg import botAction, botGoal
import actionlib
# import rospy
import time
import cv2 as cv

'''assigning separate color for simulation purpose'''
bot_color1 = (0,0,255)
bot_color2 = (0,255,0)
bot_color3 = (255, 0, 0)
bot_color4 = (125,25,205)


'''To read the csv files and store corresponding destination coordinates'''

station1,station2 = give_destination('/home/adyasha/flipkart_ws/src/Flipkart-Grid-Robotics-R2/grid_arena_r2/src/Sample Data - Sheet1.csv')


'''pseudodock for bot to wait till actual dock gets emptied'''
dock2 = [0,4]
dock1 = [0,9]
pseudodock2=[1,0]
pseudodock1=[1,13]


def fibonacci_client():
    print('init client')


    #initialise states of all bots
  
    initial1=dock2 
    initial2=dock1
    initial3=pseudodock2
    initial4=pseudodock1


    global m,n
    m=n=0
    # global station1,station2
    
    agent1_dropped = 0
    agent2_dropped = 0
    agent3_dropped = 0
    agent4_dropped = 0


    # agent1_state = [285,176]
    # agent2_state =  [296,300]
    # agent3_state = [946,176]
    # agent4_state = [946,300]
    global agent1_dest,agent2_dest,agent3_dest,agent4_dest
    agent1_dest = station1[m][2]
    agent2_dest = station2[n][2]
    agent3_dest = dock2
    agent4_dest = dock1

    while m<len(station1) and n<len(station2):
        image = cv.imread('image1.png')
       
        if type(initial1) == dict:
            initial1 = findDiscreteCoordinates(initial1)
            initial2 = findDiscreteCoordinates(initial2)
            initial3 = findDiscreteCoordinates(initial3)
            initial4 = findDiscreteCoordinates(initial4)
        
        print(agent1_dest, agent2_dest, agent3_dest, agent4_dest)
        
        schedule = find_schedule(initial1 , agent1_dest ,initial2, agent2_dest ,initial3,agent3_dest,initial4,agent4_dest)

        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")
        agent3_rc = findCoordinates(schedule,"agent2")
        agent4_rc = findCoordinates(schedule,"agent3")
        
        
        
        agent1_end = agent1_rc[-1]
        agent2_end = agent2_rc[-1]
        agent3_end = agent3_rc[-1]
        agent4_end = agent4_rc[-1]


        agent1_state = agent1_rc[0]
        agent2_state = agent2_rc[0]
        agent3_state = agent3_rc[0]
        agent4_state = agent4_rc[0]
        m,n,agent1_state,agent2_state,agent3_state,agent4_state,agent1_dropped,agent2_dropped,agent3_dropped,agent4_dropped ,agent1_dest,agent2_dest,agent3_dest,agent4_dest= complete_iter(m,n,agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped,agent3_state,agent3_rc,agent3_end,agent3_dropped,agent4_state,agent4_rc,agent4_end,agent4_dropped, agent1_dest,agent2_dest,agent3_dest,agent4_dest,image)
        
        
        initial1,initial3,agent1_dest,agent3_dest = from_where_to_where(agent1_dropped,agent1_state,agent1_dest,agent3_dropped,agent3_state,agent3_dest,dock2,pseudodock2)
        initial2,initial4,agent2_dest,agent4_dest = from_where_to_where(agent2_dropped,agent2_state,agent2_dest,agent4_dropped,agent4_state,agent4_dest,dock1,pseudodock1)

        
        
       
def complete_iter(m,n,agent1_state,agent1_rc,agent1_end,agent1_dropped,agent2_state,agent2_rc,agent2_end,agent2_dropped,agent3_state,agent3_rc,agent3_end,agent3_dropped,agent4_state,agent4_rc,agent4_end,agent4_dropped,agent1_dest,agent2_dest,agent3_dest,agent4_dest,image):
    print(m," packet from s1 ",n," packet from s2 ")
    i=j=k=l=0
   
    len1 = len(agent1_rc)
    len2 = len(agent2_rc)
    len3 = len(agent3_rc)
    len4 = len(agent4_rc)
    print("before",len1,len2,len3,len4)
    if len1==1:
        agent1_rc+=agent1_rc

    if len2==1:
        agent2_rc+=agent2_rc
    if len3==1:
        agent3_rc+=agent3_rc
    if len4==1:
        agent4_rc+=agent4_rc

    len1 = len(agent1_rc)
    len2 = len(agent2_rc)
    len3 = len(agent3_rc)
    len4 = len(agent4_rc)
    print("after",len1,len2,len3,len4)

    while i<len1-1 and j<len2-1 and k<len3-1 and l<len4-1:
            print(i,j,k,l)
            

            cv.arrowedLine(image, (agent1_state["x_c"],agent1_state["y_c"]), (agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]), bot_color1, 2)
            cv.arrowedLine(image, (agent2_state["x_c"],agent2_state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]), bot_color2, 2)
            cv.arrowedLine(image, (agent3_state["x_c"],agent3_state["y_c"]), (agent3_rc[k+1]["x_c"],agent3_rc[k+1]["y_c"]), bot_color3, 2)
            cv.arrowedLine(image, (agent4_state["x_c"],agent4_state["y_c"]), (agent4_rc[l+1]["x_c"],agent4_rc[l+1]["y_c"]), bot_color4, 2)

            cv.imshow('image',image)


            if cv.waitKey(500)==27:
                cv.destroyAllWindows()
                break


          
            if i<len1-1:
                i+=1
            if j<len2-1:
                j+=1
            if k<len3-1:
                k+=1
            if l<len4-1:
                l+=1
            agent1_state = agent1_rc[i]
            agent2_state =  agent2_rc[j]
            agent3_state = agent3_rc[k]
            agent4_state = agent4_rc[l]

            

            if findDiscreteCoordinates(agent1_state) == dock2:
                print("agent 1 home")
                agent1_dropped = 0
                m+=1
                agent1_dest = station1[m][2]
            elif agent1_state == agent1_end and findDiscreteCoordinates(agent1_state)!=pseudodock2:
                agent1_dropped = 1
                



            if findDiscreteCoordinates(agent2_state) == dock1:
                agent2_dropped = 0
                n+=1
                agent2_dest = station2[n][2]
            elif agent2_state == agent2_end and findDiscreteCoordinates(agent2_state)!=pseudodock1:
                agent2_dropped = 1
                

            if findDiscreteCoordinates(agent3_state) == dock2:
                print("agent 3 home")
                agent3_dropped = 0
                m+=1
                agent3_dest = station1[m][2]
            
            elif agent3_state == agent3_end and findDiscreteCoordinates(agent3_state)!=pseudodock2:
                agent3_dropped = 1
                



            if findDiscreteCoordinates(agent4_state) == dock1:
                print("agent 4 home")
                agent4_dropped = 0
                n+=1
                agent4_dest = station2[n][2]
            elif agent4_state == agent4_end and findDiscreteCoordinates(agent4_state)!=pseudodock1:
                agent4_dropped = 1
    print("Iteration loop done")
    return m,n,agent1_rc[i], agent2_rc[j], agent3_rc[k], agent4_rc[l], agent1_dropped, agent2_dropped, agent3_dropped, agent4_dropped,agent1_dest, agent2_dest, agent3_dest, agent4_dest


    return m, n, agent1_rc[i], agent2_rc[j], agent3_rc[k], agent4_rc[l], agent1_dropped, agent2_dropped, agent3_dropped, agent4_dropped, agent1_dest, agent2_dest, agent3_dest, agent4_dest




    


def from_where_to_where(dropped1,current1 ,dest1,dropped2,current2,dest2,dock,pseudo):
    if dropped1==0 and dropped2==0:
        initial1 = current1
        initial2 = current2
        if dest1!=dest2:
            final1 = dest1
            final2 = dest2
        else:
            final1= dest1
            final2 = pseudo
    if dropped1==1 and dropped2==1:
        initial1 = current1
        initial2 = current2
        
        final1= dock
        final2 = pseudo

    if dropped1==0 and dropped2==1:
        initial1 = current1
        initial2 = current2
        
        final1= dest1
        final2 = dock
    if dropped1==1 and dropped2==0:
        initial1 = current1
        initial2 = current2
        
        final1= dock
        final2 = dest2
    return initial1,initial2,final1,final2
    





    

if __name__ == '__main__':
    try:
       
        fibonacci_client()
    except:
        print("program interrupted before completion")
