import csv

param ={
    '1': {
            'Mumbai_alt': [3,12],
            'Delhi_alt':[7,12],
            'Kolkata_alt':[11,12],
            'Pune_alt':[2,2],
            'Ahmedabad_alt':[6,2],
            'Jaipur_alt':[10,2],
            'Mumbai': [3,9],
            'Delhi':[7,9],
            'Kolkata':[11,9],
            'Chennai':[3,8],
            'Bengaluru':[7,8],
            'Hyderabad':[11,8],
            'Pune':[3,4],
            'Ahmedabad':[7,4],
            'Jaipur':[11,4]
    },
    '2': {
        'Mumbai': [3,9],
        'Delhi':[7,9],
        'Kolkata':[11,9],
        'Chennai':[3,5],
        'Bengaluru':[7,5],
        'Hyderabad':[11,5],
        'Pune':[3,4],
        'Ahmedabad':[7,4],
        'Jaipur':[11,4]}
    }
alt_param = {
    'Mumbai_alt_alt': [4,9],
    'Delhi_alt_alt': [8,12],
    'Kolkata_alt_alt': [12,12],
    'Pune_alt_alt': [3,1],
    'Ahmedabad_alt_alt': [8,4],
    'Jaipur_alt_alt': [12,4]
}

def give_destination(file_path):

    file = open(file_path)
    csvreader = csv.reader(file)
    header = next(csvreader)
 
    rows = []
    station1 = []
    station2 = []
    for row in csvreader:
        
        if row[1]=='1':
            row[2]=param['1'][row[2]]
        
            station1.append(row)
            
            
        else:
            row[2]=param['2'][row[2]]
            station2.append(row)

    i=j=0
    if len(station1)<len(station2):
        l = len(station1)
    else:
        l = len(station2)


    while i<l:
        if station1[i][2]==station2[i][2]:
           
            x = station1[i][2]
            for key in param['1']:
                if param['1'][key] == x:
                    station1[i][2] = param['1'][key+'_alt']

        i+=1


    file.close()
    return [station1,station2]


