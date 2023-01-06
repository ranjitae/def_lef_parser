import json

# from def_parser import parse_def
from fulladder_lef_pins_prog import parse_lef
from fulladderdef_lef_merge import merge_def_lef

def merge_def_lef1(input1, input2, output):
    merge_def_lef(input1,input2,'merge_out.json')
    # parse_def(input1, 'def_out_dd1.json')
    parse_lef(input2, 'fulldder_lef_pins.json')

    with open('merge_out.json') as def_json:
        def_dict = json.load(def_json)

    with open('fulldder_lef_pins.json') as lef_json:
        lef_dict = json.load(lef_json)

    merge_dict = def_dict

    for cell in lef_dict['cells']:
        for count, defcell in enumerate(def_dict['components']):
            # print(defcell['ref_name'],cell['ref_Name'])
            if defcell['ref_name'] == cell['ref_Name']:
                merge_dict['components'][count]['pins'] = cell['Pins']
    
    

            
               
    with open(output, 'w') as outfile:
        json.dump(merge_dict, outfile, indent=4)

    return output

merge_def_lef1('fulladder_V0.1.def', 'fulladder_V0.1.lef.txt', 'fulladder_lefpins_deffile_merger_out1.json')

import json
import os

filename = 'fulladder_lefpins_deffile_merger_out1.json'
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
                a =y3-j['Route'][0]
                b=y4 -j['Route'][1]
                j['p1']=a
                j['p2']=b



os.remove(filename)
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)








