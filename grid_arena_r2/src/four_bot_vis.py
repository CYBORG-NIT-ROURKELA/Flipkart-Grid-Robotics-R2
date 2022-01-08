#! /usr/bin/env python
"""
Created on Wed Jan 05 20:33:59 2022

@author: Adyasha
"""
from destination import give_destination
from schedule import find_schedule
from centroids import findCoordinates, findDiscreteCoordinates
import time
from grid_arena_r2.msg import botAction, botGoal
import actionlib
import cv2 as cv
from copy import deepcopy

'''assigning separate color for simulation purpose'''
bot_color1 = (0,255,0)
bot_color2 = (255,0,0)
bot_color3 = (0, 0, 255)
bot_color4 = (25,127,127)

'''To read the csv files and store corresponding destination coordinates'''

station1,station2 = give_destination('/home/adyasha/flipkart_ws/src/Flipkart-Grid-Robotics-R2/grid_arena_r2/src/Sample Data - Sheet1.csv')

'''pseudodock for bot to wait till actual dock gets emptied'''

dock2 = [0,4]
dock1 = [0,9]
pseudodock2=[1,0]
pseudodock1=[1,12]

class Bot:
    def __init__(self,start,drop_state,dest,home,pseudohome):
        self.initial = start
        self.dropped = drop_state
        self.destination = dest
        self.dock = home
        self.pseudodock = pseudohome
        self.last = None
        self.state = self.initial
        

    def update(self,coordinate_list):
        self.last = coordinate_list[-1]
        self.state = coordinate_list[0]

    def __str__(self):
        return "initial coord: "+str(self.initial) + "      destination coord: "+str(self.destination) + "      dropped status: "+str(self.dropped) + "     last coord: " + str(findDiscreteCoordinates(self.last)) + "      state: " + str(findDiscreteCoordinates(self.state))

def fibonacci_client():
    print('init client')
    global m,n
    m=n=0

    agent1 = Bot(dock2,0,station1[m][2],dock2,pseudodock2)
    agent2 = Bot(dock1,0,station2[n][2],dock1,pseudodock1)
    agent3 = Bot(pseudodock2,0,dock2,dock2,pseudodock2)
    agent4 = Bot(pseudodock1,0,dock1,dock1,pseudodock1)
    # print(str(agent2))
    # print(str(agent4))
    # time.sleep(5)

    while m<len(station1) and n<len(station2):
        
        
        image = cv.imread('image1.png')
     
        if type(agent1.initial) == dict:
            agent1.initial = findDiscreteCoordinates(agent1.initial)
            agent2.initial = findDiscreteCoordinates(agent2.initial)
            agent3.initial = findDiscreteCoordinates(agent3.initial)
            agent4.initial = findDiscreteCoordinates(agent4.initial)
        
        schedule = find_schedule(agent1.initial , agent1.destination ,agent2.initial, agent2.destination ,agent3.initial,agent3.destination,agent4.initial,agent4.destination)
       
        agent1_rc = findCoordinates(schedule,"agent0")
        agent2_rc = findCoordinates(schedule,"agent1")
        agent3_rc = findCoordinates(schedule,"agent2")
        agent4_rc = findCoordinates(schedule,"agent3")
        
        agent1.update(agent1_rc)
        agent2.update(agent2_rc)
        agent3.update(agent3_rc)
        agent4.update(agent4_rc)
       
        m,n = complete_iter(m,n,agent1_rc,agent1,agent2_rc,agent2,agent3_rc,agent3,agent4_rc,agent4,image)
        from_where_to_where(agent1,agent1.state,agent3,agent3.state,dock2,pseudodock2)
        from_where_to_where(agent2,agent2.state,agent4,agent4.state,dock1,pseudodock1)
            
def complete_iter(m,n,agent1_rc,agent1,agent2_rc,agent2,agent3_rc,agent3,agent4_rc,agent4,image):

    print(m+1," packet from station 1 ",n+1," packet from station 2 ")
    # print 
    # print(m+1,"packet from station 1")
    print("agent1  ",str(agent1))
    print ("agent2  ",str(agent2))
    print ("agent3  ",str(agent3))
    print ("agent4  ",str(agent4))
    

    i=j=k=l=0

    len1 = append_coordinates(agent1_rc)
    len2 = append_coordinates(agent2_rc)
    len3 = append_coordinates(agent3_rc)
    len4 = append_coordinates(agent4_rc)
    client = actionlib.SimpleActionClient('botAction_1', botAction)
    client_2 = actionlib.SimpleActionClient('botAction_2', botAction)
    client_3= actionlib.SimpleActionClient('botAction_3', botAction)
    client_4 = actionlib.SimpleActionClient('botAction_4', botAction)

    client.wait_for_server()
    print("client 1 connected")
    client_2.wait_for_server()
    print("client 1 connected")
    client_3.wait_for_server()
    print("client 1 connected")
    client_4.wait_for_server()
    print("client 1 connected")


   
    while i<len1-1 and j<len2-1 and k<len3-1 and l<len4-1:
            image = cv.imread("image1.png")
    
            cv.arrowedLine(image, (agent1.state["x_c"],agent1.state["y_c"]), (agent1_rc[i+1]["x_c"],agent1_rc[i+1]["y_c"]), bot_color1, 2)
            cv.arrowedLine(image, (agent2.state["x_c"],agent2.state["y_c"]), (agent2_rc[j+1]["x_c"],agent2_rc[j+1]["y_c"]), bot_color2, 2)
            cv.arrowedLine(image, (agent3.state["x_c"],agent3.state["y_c"]), (agent3_rc[k+1]["x_c"],agent3_rc[k+1]["y_c"]), bot_color3, 2)
            cv.arrowedLine(image, (agent4.state["x_c"],agent4.state["y_c"]), (agent4_rc[l+1]["x_c"],agent4_rc[l+1]["y_c"]), bot_color4, 2)

            cv.imshow('image',image)

            if cv.waitKey(50)==27:
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
            agent1.state = agent1_rc[i]
            agent2.state =  agent2_rc[j]
            agent3.state = agent3_rc[k]
            agent4.state = agent4_rc[l]

            m=update_next_goal(agent1,m,station1)
            n=update_next_goal(agent2,n,station2)
            m=update_next_goal(agent3,m,station1)
            n=update_next_goal(agent4,n,station2)

    return m,n

def from_where_to_where(agent_a,current1,agent_b,current2,dock,pseudo):

    if agent_a.dropped==0 and agent_b.dropped==0:  
        if agent_a.destination!=agent_b.destination:
            
            final1 = agent_a.destination
            final2 = agent_b.destination
        else:
          
            print(agent_a.destination,agent_b.destination)
            agent_a.destination = deepcopy(agent_b.destination)
            agent_a.destination[0] += 1
            
            final1 = agent_a.destination
            final2 = agent_b.destination
            print(final1,final2)
    if agent_a.dropped==1 and agent_b.dropped==1:
        final1= dock
        final2 = pseudo

    if agent_a.dropped==0 and agent_b.dropped==1:   
        final1= agent_a.destination
        final2 = dock

    if agent_a.dropped==1 and agent_b.dropped==0:
        final1= dock
        final2 = agent_b.destination

    agent_a.initial = current1
    agent_a.destination = final1
    agent_b.initial = current2
    agent_b.destination = final2

'''update single coordinate list'''

def append_coordinates(goal_list):
    if len(goal_list)==1:
        goal_list+=goal_list
    return len(goal_list)

'''update goals after any agent completes destination list'''

def update_next_goal(agent,iter,station):
    if findDiscreteCoordinates(agent.state) == agent.dock:
        print("agent home")
        agent.dropped = 0
        iter+=1
        agent.destination = station[iter][2]
    elif agent.state == agent.last and findDiscreteCoordinates(agent.state)!=agent.pseudodock:
        agent.dropped = 1
    return iter   

if __name__ == '__main__':
    try:
       
        fibonacci_client()
       
    except:
        print("program interrupted before completion")
