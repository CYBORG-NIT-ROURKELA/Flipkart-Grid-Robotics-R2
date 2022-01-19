

from coordinates import cordinates, reverse_mapping

rev_coords = reverse_mapping(cordinates)

# start_x = 225
# start_y = 696
# d_x = 51.5
# d_y = 47.5

# start_x = 54
# start_y = 460
# d_x = 36.2
# d_y = 36.5


# schedule = {}

# def findCoordinates(list,agent):
#     input = list
#     points = input["schedule"][agent]

    
#     schedule_list = [{'t':i["t"], 'x_c':int(start_x+(i["x"]*d_x)), 'y_c':int(start_y-(i["y"]*d_y))} for i in points]
        
#     return schedule_list


# def findDiscreteCoordinates(a):#{'y_c': 648, 't': 9, 'x_c': 534}   [7,4]
#     discrete = [int(round((a['x_c']-start_x)/d_x)),int(round((start_y-a['y_c'])/d_y))]
#     return discrete

    
# def RealToDiscrete(a):
#     return [int(round((a[0]-start_x)/d_x)), int(round((start_y-a[1])/d_y))]
# def findRealCoordinates(list):
#     return [int(start_x+(list[0]*d_x)), int(start_y-(list[1]*d_y))]

def findCoordinates(list,agent):
    input = list
    points = input["schedule"][agent]
    schedule_list = [{'t':i["t"], 'x_c':cordinates[(i["x"], i["y"])][0], 'y_c':cordinates[(i["x"], i["y"])][1]} for i in points] 
    return schedule_list
    
def findDiscreteCoordinates(a):#{'y_c': 648, 't': 9, 'x_c': 534}   [7,4]
    discrete = rev_coords[(a['x_c'], a['y_c'])]
    return discrete

def RealToDiscrete(a):
    return rev_coords[(a[0], a[1])]

def findRealCoordinates(list):
    return cordinates[tuple(list)]