import json

from def_parser import parse_def
from lef_parser import lef_parser

def merge_def_lef(input1, input2, output):
    parse_def(input1, 'def_out.json')
    lef_parser(input2, 'lef_out.json')

    with open('def_out.json') as def_json:
        def_dict = json.load(def_json)

    with open('lef_out.json') as lef_json:
        lef_dict = json.load(lef_json)

    merge_dict = def_dict

    for cell in lef_dict:
        for count, defcell in enumerate(def_dict['components']):
            if cell['ref_name'] == defcell['ref_name']:
                merge_dict['components'][count]['x1'] = merge_dict['components'][count]['x']+cell["cellsize"]["width"]
                merge_dict['components'][count]['y1'] = merge_dict['components'][count]['y']+cell["cellsize"]["height"]
            
    with open(output, 'w') as outfile:
        json.dump(merge_dict, outfile, indent=4)

    return output

merge_def_lef('fulladder_V0.1.def', 'fulladder_V0.1.lef.txt', 'merge_out.json')


