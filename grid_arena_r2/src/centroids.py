import argparse
import yaml

start_x = 311
start_y = 637
d_x = 40
d_y = 38
schedule = {}
def findCoordinates(list,agent):
    input = list
    points = input["schedule"][agent]

    
    schedule_list = [{'t':i["t"], 'x_c':start_x+(i["x"]*d_x), 'y_c':start_y-(i["y"]*d_y)} for i in points]
        
    return schedule_list
    
    

