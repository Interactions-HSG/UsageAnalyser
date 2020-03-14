import csv
with open('input/outputTableMar-04-2020_110846.csv','rt')as f:
    data = csv.reader(f)
    furniture_name=[]
    furniture_usage=[]
    for row in data:
        furniture_name.append(row[1])
        furniture_usage.append(row[2])
    usageDict=dict(zip(furniture_name,furniture_usage))
    
    print(usageDict)
  
    
