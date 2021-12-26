agent1_path = [{'t': 0, 'x_c': 0, 'y_c': 10}, {'t': 1, 'x_c': 1, 'y_c': 10}, {'t': 2, 'x_c': 1, 'y_c': 9}, {'t': 3, 'x_c': 2, 'y_c': 9}, {'t': 4, 'x_c': 2, 'y_c': 8}]

agent0_path = [{'t': 0, 'x_c': 0, 'y_c': 5}, {'t': 1, 'x_c': 1, 'y_c': 5}, {'t': 2, 'x_c': 1, 'y_c': 6}, {'t': 3, 'x_c': 1, 'y_c': 7}, {'t': 4, 'x_c': 1, 'y_c': 8}, {'t': 5, 'x_c': 1, 'y_c': 9}, {'t': 6, 'x_c': 1, 'y_c': 10}, {'t': 7, 'x_c': 1, 'y_c': 11}, {'t': 8, 'x_c': 2, 'y_c': 11}]

def call_cbs(agent0_path,agent1_path):
    i=j=0
    i_end = len[agent0_path]-1
    j_end = len[agent1_path]-1

    agent0_last = agent0_path[len[agent0_path]-1]
    agent1_last = agent1_path[len[agent1_path]-1]
    agent0_state = agent0_path[i]
    agent1_state = agent1_path[j]


    while agent0_state!=agent0_last | agent1_state!=agent1_last:
         maneuver(agent0_state,agent0_path[i+1],agent1_state,agent1_path[j+1])
         if i!=i_end:
             i+=1
         if j!=j_end:
             j+=1
         agent0_state = agent0_path[i]
         agent1_state = agent1_path[j]

         
    

   

def maneuver(a,b):
    """each coordinate start,end along with IP return bool"""
    pass
call_cbs(agent0_path,agent1_path)





