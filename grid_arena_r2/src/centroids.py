import argparse
import yaml

start_x = 225
start_y = 696
d_x = 51.5
d_y = 47.5
schedule = {}
def findCoordinates(list,agent):
    input = list
    points = input["schedule"][agent]

    
    schedule_list = [{'t':i["t"], 'x_c':int(start_x+(i["x"]*d_x)), 'y_c':int(start_y-(i["y"]*d_y))} for i in points]
        
    return schedule_list
    
    

