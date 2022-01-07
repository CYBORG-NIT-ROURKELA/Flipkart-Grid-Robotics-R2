

# start_x = 225
# start_y = 696
# d_x = 51.5
# d_y = 47.5

start_x = 54
start_y = 460
d_x = 36.2
d_y = 36.5


schedule = {}

def findCoordinates(list,agent):
    input = list
    points = input["schedule"][agent]

    
    schedule_list = [{'t':i["t"], 'x_c':int(start_x+(i["x"]*d_x)), 'y_c':int(start_y-(i["y"]*d_y))} for i in points]
        
    return schedule_list


def findDiscreteCoordinates(a):#{'y_c': 648, 't': 9, 'x_c': 534}   [7,4]
    discrete = [int(round((a['x_c']-start_x)/d_x)),int(round((start_y-a['y_c'])/d_y))]
    return discrete

    
def RealToDiscrete(a):
    return [int(round((a[0]-start_x)/d_x)), int(round((start_y-a[1])/d_y))]
