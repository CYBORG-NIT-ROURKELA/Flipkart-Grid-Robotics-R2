from coordinates import cordinates, reverse_mapping
from copy import deepcopy

rev_coords = reverse_mapping(cordinates)

def findCoordinates(list,agent):
    input = list
    points = input["schedule"][agent]
    schedule_list = [{'t':i["t"], 'x_c':cordinates[(i["x"], i["y"])][0], 'y_c':cordinates[(i["x"], i["y"])][1]} for i in points]
    return schedule_list

def findDiscreteCoordinates(a):  #{'y_c': 648, 't': 9, 'x_c': 534} => [7,4]
    discrete = deepcopy(rev_coords[(a['x_c'], a['y_c'])])
    return discrete

def RealToDiscrete(a):
    return rev_coords[(a[0], a[1])]

def findRealCoordinates(list):
    return cordinates[tuple(list)]
