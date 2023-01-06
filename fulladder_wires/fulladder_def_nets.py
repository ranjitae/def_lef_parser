import json

def parse_def(input, output):
    main_dict = {} 
    nets=[]
    # pin = []
    
    i = 0
    num = 0
    #opened file in read mode
    with open(input) as f:
        lines = f.read().splitlines() 
        for count,line in enumerate(lines):    
            if line.startswith('DESIGN'):
                line = line.split()
                main_dict['design'] = line[1]
            elif line.startswith('NETS'):
                start_index = count
                line1 = line.split(' ')
                main_dict['number_of_nets']=int(line1[1])
            elif line.startswith('END NETS'):
                end_index = count+1

                # reading start nets to end nets
                
                for i in range(start_index, end_index):
                    # print(lines[i])
                    
          
                    if lines[i].startswith('-'):
                        n = (lines[i].split()[1])
                        # print(n)
                        start = i+1
                        # print("start",start)
                        # nets.append({"net name":n,"connection":instance})  #,"connection":cell_pin})
                        # print(regs_start)
                    elif lines[i].strip().startswith("+ ROUTED"):
                        end = i
                        # print("end",end)
                    # for route end
                    elif lines[i].strip().startswith("+ USE"):
                        route_end = i
                    
                        instance=[]
                        pins={}
                        # start lines from nets name to +route
                        for i in range(start,end):
                            # print(lines[i])
                            
                            if lines[i].strip().startswith("( PIN"):   
                                p = (lines[i].split()[-2])
                                pins.update({"design_pin":p})
                                # print(p)
                                
                            else:
                                iname = lines[i].split()[1]
                                pname = lines[i].split()[2]
                                instance.append({"instance name":iname,"pin":pname})
                                if pins!={}:

                                    instance.append(pins)
                        # for route 
                        
                        # start from + Route to + USE
                        route =[]
                        num1 = 0
                        for i in range(end,route_end+1):
                            
                            # print(lines[i])
                            if lines[i].strip().startswith("+ ROUTED"):
                                l1 = lines[i].split(" ")
                                layer = l1[5]
                                # print(l1)
                                # x = 10
                                # print(type(x))
                                line = []
                                for i in l1:
                                    # print(i)
                                    if i.startswith('VIA'):
                                        break
                                    
                                    elif i.isdigit() or i == '*':
                                        line.append(i)
                                for i in range(len(line)):        
                                    if '*' in line:
                                        p = line.index('*')
                                        line[p] = line[p-2]
                                    # print(line[p])
                                # print('x  :',line[0],'y ;'line[1])
                                # for i in range(0,len(line),2):
                                #     print('x  : ',line[i],'y  : ',line[i+1]) 
                                # print('------------------')
                                      
                                line = list(map(int,line))
                                l = {}
                                a = 0
                                for i in range(0,len(line),2):
                                    l.update({f'x{a}':line[i],f'y{a}':line[i+1]})
                                    a = a+1
                                    
                                route.append({'id':num1,"layer":layer,"line":l})
                               
                            elif lines[i].strip().startswith("NEW"):
                                # print(lines[i])
                                l2 = lines[i].split(" ")
                                layer1 = l2[4]
                                # print(l2)
                                line1 = []
                                for i in l2:
                                    if i.startswith('VIA'):
                                        break
                                    elif i.isdigit() or i == '*':

                                        line1.append(i)
                                for i in range(len(line1)):
                                    if line1[i] == '*':
                                        p1 = line1.index('*')
                                        line1[p1] = line1[p1-2]
                                
                                line1 = list(map(int,line1))
                                l1 = {}
                                a = 0
                                for i in range(0,len(line1),2):
                                    l1.update({f'x{a}':line1[i],f'y{a}':line1[i+1]})
                                    a = a+1    
                                route.append({'id' : num1,"layer":layer1,"line":l1})
                            num1 = num1+1   
                        num = num +1    
                        nets.append({'id': num,
                            "net name":n,
                        "connection":instance,
                        "route" : route

                        })


    # main_dict["pins"] = pin
    main_dict['nets']=nets

  
    with open(output, 'w') as output1:

        # nets.append({"net name":n})

        json.dump(main_dict, output1, indent=4)
    return output

parse_def('fulladder_V0.1.def', 'fulladder_def_wires.json')


















