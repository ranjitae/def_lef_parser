import json
import os

filename = 'merge_out1.json'
with open(filename, 'r') as f:
    data = json.load(f)
    x = data['components']
    for i in data['components']:
        # print(i)
        y1 = i['x']
        y2 = i['y']
        y3 = i['x1']
        y4 = i['y1']
        # print(y1,y2,y3,y4)
        a =0
        b= 0
        for c,j in enumerate(i['pins']):
            if j['direction'] == 'INPUT':
                a =j['Route'][0]+y1
                b=j['Route'][1]+y2
                j['p1']=a
                j['p2']=b
            elif j['direction'] == 'INOUT':
                a =j['Route'][0]+y1
                b=j['Route'][1]+y2
                j['p1']=a
                j['p2']=b
            elif j['direction'] == 'OUTPUT':
                a =j['Route'][0]+y3
                b=j['Route'][1]+y4
                j['p1']=a
                j['p2']=b



os.remove(filename)
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)