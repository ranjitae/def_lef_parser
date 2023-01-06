import json
import sys
import numpy as np
def lef_parser(input, output):
    input_file=open(input,'r')
    input_content=input_file.readlines()
    cell_name=[]
    cell_size=[]
    pins =[]
    unit=[]
    data={}
    #function to seperate the data and store 
    def check_data(input_data,key_word,store_data):
        if input_data.strip().startswith(key_word):
            store_data.append(i.split()[1:])

    #iteration through the text file content       
    for i in input_content:
        if i.strip().startswith('DATABASE MICRON'):
            unit=float(i.split()[2])
        check_data(i,'MACRO',cell_name)
        check_data(i,'SIZE',cell_size)
        check_data(i,'PIN',pins)

    #creating the outfile in json format

    def clean_cell_size(input_data2,index_value):
        return list(np.float_(' '.join(input_data2).strip(';').split('BY')))[index_value]*unit

    with open(output, 'w') as outfile:
    
        data= [
            {'ref_name' : cell_name[i][0], 

                'cellsize' :

                    {'cell size':' '.join(cell_size[i][0:-1]),
                        'width':clean_cell_size(cell_size[i],0),
                        'height':clean_cell_size(cell_size[i],1)}}
                        for i in range(len(cell_name))]
    
        return json.dump(data, outfile,indent=4)
lef_parser('fulladder_V0.1.lef.txt', 'lef_out.json')