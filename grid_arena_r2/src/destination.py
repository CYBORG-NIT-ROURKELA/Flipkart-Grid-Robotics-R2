import csv

def give_destination(file_path):
    param ={'1':{'Mumbai': [3,9],'Delhi':[7,9],'Kolkata':[11,9],'Chennai':[3,8],'Bengaluru':[7,8],'Hyderabad':[11,8],'Pune':[3,4],'Ahmedabad':[7,4],'Jaipur':[11,4]},
            '2': {'Mumbai': [3,9],'Delhi':[7,9],'Kolkata':[11,9],'Chennai':[3,5],'Bengaluru':[7,5],'Hyderabad':[11,5],'Pune':[3,4],'Ahmedabad':[7,4],'Jaipur':[11,4]}}


    file = open(file_path)
    csvreader = csv.reader(file)
    header = next(csvreader)
    print(header)
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

    file.close()
    return [station1,station2]



