from cbs import Environment,CBS


# def find_schedule(start_1,goal_1,start_2,goal_2,start_3,goal_3,start_4,goal_4):

#     param = {'map':{'dimensions' : [15,14],'obstacles' : [(0,0),(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),(0,12),(0,13),(3, 2), (4, 2), (3, 3), (4, 3), (7, 2), (8, 2), (7, 3), (8, 3), (11, 2), (12, 2), (11, 3), (12, 3), (3, 6), (4, 6), (3, 7), (4, 7), (3, 10), (4, 10), (3, 11), (4, 11), (7, 6), (8, 6), (7, 7), (8, 7), (7, 10), (8, 10), (7, 11), (8, 11), (11, 6), (12, 6), (11, 7), (12, 7), (11, 10), (12, 10), (11, 11), (12, 11)]
#     }}
#     params ={'agents': [{'start': start_1, 'goal': goal_1, 'name': 'agent0'}, {'start': start_2, 'goal': goal_2, 'name': 'agent1'},{'start': start_3, 'goal': goal_3, 'name': 'agent2'},{'start': start_4, 'goal': goal_4, 'name': 'agent3'}]}
#     dimension = param["map"]["dimensions"]
#     obstacles = param["map"]["obstacles"]
#     agents = params['agents']




#     env = Environment(dimension, agents, obstacles)

#     # Searching
#     cbs = CBS(env)
#     solution = cbs.search()
#     if not solution:
#         print(" Solution not found" )
#         return

#     # Write to output file
#     output = {}

#     output["schedule"] = solution
#     output["cost"] = env.compute_solution_cost(solution)
#     return output

def find_schedule2(start_1,goal_1,start_2,goal_2):

    param = {'map':{'dimensions' : [15,14],'obstacles' : [(0,0),(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),(0,12),(0,13),(3, 2), (4, 2), (3, 3), (4, 3), (7, 2), (8, 2), (7, 3), (8, 3), (11, 2), (12, 2), (11, 3), (12, 3), (3, 6), (4, 6), (3, 7), (4, 7), (3, 10), (4, 10), (3, 11), (4, 11), (7, 6), (8, 6), (7, 7), (8, 7), (7, 10), (8, 10), (7, 11), (8, 11), (11, 6), (12, 6), (11, 7), (12, 7), (11, 10), (12, 10), (11, 11), (12, 11)]
    }}
    params ={'agents': [{'start': start_1, 'goal': goal_1, 'name': 'agent0'}, {'start': start_2, 'goal': goal_2, 'name': 'agent1'}]}
    dimension = param["map"]["dimensions"]
    obstacles = param["map"]["obstacles"]
    agents = params['agents']
    env = Environment(dimension, agents, obstacles)

    # Searching
    cbs = CBS(env)
    solution = cbs.search()
    if not solution:
        print(" Solution not found" )
        return

    # Write to output file
    output = {}

    output["schedule"] = solution
    output["cost"] = env.compute_solution_cost(solution)
    return output

def find_schedule2(start_1,goal_1,start_2,goal_2):

    param = {'map':{'dimensions' : [15,14],'obstacles' : [(0,0),(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),(0,12),(0,13),(3, 2), (4, 2), (3, 3), (4, 3), (7, 2), (8, 2), (7, 3), (8, 3), (11, 2), (12, 2), (11, 3), (12, 3), (3, 6), (4, 6), (3, 7), (4, 7), (3, 10), (4, 10), (3, 11), (4, 11), (7, 6), (8, 6), (7, 7), (8, 7), (7, 10), (8, 10), (7, 11), (8, 11), (11, 6), (12, 6), (11, 7), (12, 7), (11, 10), (12, 10), (11, 11), (12, 11)]
    }}
    params ={'agents': [{'start': start_1, 'goal': goal_1, 'name': 'agent0'}, {'start': start_2, 'goal': goal_2, 'name': 'agent1'}]}
    dimension = param["map"]["dimensions"]
    obstacles = param["map"]["obstacles"]
    agents = params['agents']




    env = Environment(dimension, agents, obstacles)

    # Searching
    cbs = CBS(env)
    solution = None
    i = 0
    while not solution:
        solution = cbs.search()
        i+=1
        if i == 10:
            break
    if not solution:
        print(" Solution not found" )
        return

    # Write to output file
    output = {}

    output["schedule"] = solution
    output["cost"] = env.compute_solution_cost(solution)
    return output

