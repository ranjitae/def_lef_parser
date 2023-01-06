import json


def parse_lef(input, output):
    main_dict = {}
    index_end = 0 
    nets =[]
    x = 0
    
    
    #opened file in read mode
    with open(input) as f:
        lines = f.readlines()
        # iterating over each line
        for line in lines:
            if line.startswith('VERSION'):
                line = line.split()
                main_dict['VERSION'] = line[1]
            elif line.startswith('BUSBITCHARS'):
                line = line.strip().split(" ")
                new_list = [item.replace('"', '') for item in line]
                main_dict['BUSBITCHARS'] = new_list[1]
            elif line.startswith('DIVIDERCHAR'):
                line = line.strip().split()
                new_list = [item.replace('"', '') for item in line]
                main_dict['DIVIDERCHAR'] = new_list[1]
            elif line.startswith('MANUFACTURINGGRID'):
                line = line.strip().split()
                main_dict['MANUFACTURINGGRID'] = line[1]
                    
            # getting line containg COMPONENTS and getting start and end index
            elif line.startswith('MACRO'):
                line1 = line.split(" ")
                index_start = lines.index(line)
                cell_name= line1[1]
                # print(f'END {cell_name}')
                # print(lines)
                index_end = lines.index(f'END {cell_name}')
                # print(index_end)
                pin =[]
            
                size ={}
                class_1 =''
                foreign =''
                site = ''
                sym = ''
                f =0
                # print(index_start)
                # print(line1)
            
                # getting the pins from each cell
                pin_name = ""
                for a in range(index_start, index_end):
                    # print(lines[a])
                    if lines[a].strip().startswith('CLASS'):
                            # print(lines[a])
                        d = lines[a].strip().split()[1]
                        class_1=str(d)
                    elif lines[a].strip().startswith('FOREIGN'):
                            # print(lines[a])
                        d = lines[a].strip().split()[1]
                        # d.pop('[')
                        # d.pop()
                        foreign = str(d)
                        # print(d)
                    elif lines[a].strip().startswith('SIZE'):
                            # print(lines[a])
                        d = lines[a].strip().split()
                        
                        size.update({
                            'x':float(d[1])*1000,'y':float(d[3])*1000

                        })
                    elif lines[a].strip().startswith('SITE'):
                            # print(lines[a])
                        d = lines[a].strip().split()[1]
                        site=str(d)
                    elif lines[a].strip().startswith('SYMMETRY'):
                            # print(lines[a])
                        d = lines[a].strip().split()[1:3]
                        c = ' '.join(d)
                        sym=str(c)

                    elif lines[a].strip().startswith('PIN'):
                        index_pinstart = lines.index(lines[a])
                        pin_name = str(lines[a].strip().split()[1])

                    elif lines[a].strip().startswith(f'END {pin_name}'):
                        endin = lines.index(lines[a])
                        # print(endin)
                        x_list = []
                        x_final =[]
                        
                        for o in range(index_pinstart,endin):
                            
                            if lines[o].strip().startswith('DIRECTION'):
                                # print(lines[o])
                                x3 = lines[o].split(' ')[-2]
                                # print(x3[-2])
                    
                            elif lines[o].strip().startswith('USE'):
                                x4= lines[o].split(' ')

                            elif lines[o].strip().startswith('LAYER'):
                                x6 = lines[o].strip().split(" ")[1]

                            elif lines[o].strip().startswith('RECT'):
                                x5 = lines[o].strip().split(" ")
                        
                                x5.remove("")
                                x5.remove('RECT')
                                x5.pop()
                                x_list1 = [float(i) for i in x5]
                                    
                                x_list.append({'rect':x_list1})
                            
                        # print(x_list)   
                        a =0
                        x =0
                        y =0
                        for i in x_list:
                            x += i['rect'][0]
                            x += i['rect'][2]
                            y += i['rect'][1]
                            y += i['rect'][3]
                            # print(i['rect'][2])
                            a+= 1
                        
                        x=x/(a*2)
                        y=y/(a*2)
                        # print(x,y)
                        
                        x_final.append(round(x*100,2))
                        x_final.append(round(y*100,2))
                        pin.append({
                            "id": f,
                            "pin_name":pin_name,
                            "direction" : x3,
                            "use" : x4[-2],
                            'layer':x6,
                            'Route':x_final,
                        }) 
                        f +=1
                        
                        
                nets.append({
                'ref_Name':cell_name.strip(),
                'CLASS':class_1,
                'FOREIGN': foreign,
                'SIZE':size,
                'SYMMETRY': sym,
                'SITE': site,
                'Pins': pin})   

                 
         
    main_dict['cells']= nets
    main_json = json.dumps(main_dict, indent=4)

    # dumoing into json file
    with open(output, 'w') as output1:
        json.dump(main_dict, output1, indent=4)
    return output

parse_lef('fulladder_V0.1.lef.txt', 'fulladder_lef_pins.json')



# if len(main_dict)!=main_dict['number_of_nets']:
    #     print('There are {} missing nets'.format(main_dict['number_of_nets']-len(main_dict['nets'])))
        
