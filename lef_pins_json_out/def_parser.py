import json

def parse_def(input, output):
    main_dict = {}
    index_end = 0 
    components = []                          # it was throwing error in py file so initialized it here
    #opened file in read mode
    with open(input) as f:
        lines = f.readlines()
        # iterating over each line
        i=0 
        for line in lines:
            if line.startswith('DESIGN'):
                line = line.split()
                main_dict['design'] = line[1]

            elif line.startswith('UNITS DISTANCE'):
                line1 = line.split(" ")
                main_dict['unit_in_micron']=float(line1[3])
                # converting co-oradinate values
                mul_unit = main_dict['unit_in_micron']*(10**-3)
                
            # getting line containing die area
            elif line.startswith('DIEAREA'):
                line1 = line.split(" ")
                # print(line1)
                if len(line1)<12:
                    main_dict['diearea'] = {
                                        'x1':float(line1[2])*mul_unit,
                                        'y1':float(line1[3])*mul_unit,
                                        'x2':float(line1[6])*mul_unit,
                                        'y2':float(line1[7])*mul_unit
                                        }
                else:
                    main_dict['diearea'] = {
                                            'x1':float(line1[2])*mul_unit,
                                            'y1':float(line1[3])*mul_unit,
                                            'x2':float(line1[6])*mul_unit,
                                            'y2':float(line1[7])*mul_unit,
                                            'x3':float(line1[10])*mul_unit,
                                            'y3':float(line1[11])*mul_unit,
                                            'x4':float(line1[14])*mul_unit,
                                            'y4':float(line1[15])*mul_unit
                                            }
                    
            # getting line containg COMPONENTS and getting start and end index
            elif line.startswith('COMPONENTS'):
                line1 = line.split(" ")
                index_start = lines.index(line)
                index_end = lines.index('END COMPONENTS\n')
                main_dict['number_of_components']=int(line1[1])
            
            # lines containing component part with start and end index
            
            elif lines.index(line)<index_end and lines.index(line)>index_start:
                line3 = line.split()
                
                def parse_components(word):
                    if word in line3:
                        components.append({
                                    'Comp_id':i,
                                    'ref_name':line3[2],
                                    'instance_name':line3[1],
                                    'x':float(line3[line3.index(word)+2])*mul_unit,
                                    'y':float(line3[line3.index(word)+3])*mul_unit,
                                    'direction':line3[line3.index(word)+5]                           
                                    })
                def parse_components1(word):
                    if word in line3:
                        components.append({
                                    'Comp_id':i,
                                    'ref_name':line3[2],
                                    'instance_name':line3[1],
                                    'x':'-',
                                    'y':'-',
                                    'direction':'-'                           
                                    })
                
                
                parse_components('COVER')
                parse_components('FIXED')
                parse_components('PLACED')
                parse_components1('UNPLACED')
                i+=1
    main_dict['components']=components
    main_json = json.dumps(main_dict, indent=4)

    # print(len(main_dict['components']))
    # print(main_dict['number_of_components'])
    # if len(main_dict)!=main_dict['number_of_components']:
    #     print('There are {} missing components'.format(main_dict['number_of_components']-len(main_dict['components'])))
        
    with open(output, 'w') as output1:
        json.dump(main_dict, output1, indent=4)
    return output

parse_def('fulladder_V0.1.def', 'def_out_dd1.json')