#coding: utf-8
"""
Main programm to test firstly
"""
import api_scade.scade_suite_file as sc
from model.block_port_link import Block, InputPort, OutputPort, Link
import scade_env
import scade.model.suite, scade.model.project

import re

COLOR = ["blue","red","orange","green"]

PATH_SESSION = r"C:\TRAVAIL\BCM_WIP\V1\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\MASTER\MASTER.etp"


def main():
    """ main programm """
    list_of_to_file = []
    list_of_inputs = []
    list_of_outputs = []
    list_of_block = []

    scade_env.load_project(PATH_SESSION)
    a = scade.model.suite.get_roots()[0]
    scade_object = sc.ScadeFileSuite(a)
    # data = scade_object.data_of_interest()
    data = scade_object.data_of_nodes()

    # for i,color in zip(data,COLOR):
    #     for j in data[i]:
    #         b = Block(j,color)
    #         for input in data[i][j]['inputs']:
    #             v = InputPort(b,input + re.findall(r'^d\d+',j)[0])
    #             list_of_inputs.append(v)
    #         for output in data[i][j]['outputs']:
    #             vv = OutputPort(b,output + re.findall(r'^d\d+',j)[0])
    #             list_of_outputs.append(vv)
    #         list_of_to_file.append(b.write_block_w_port())
    #         list_of_block.append(b)

    for i,color in zip(data,COLOR):
        b = Block(i,color)
        for input in data[i]['inputs']:
            v = InputPort(b,input + re.findall(r'_P\d+',i)[0])
            list_of_inputs.append(v)
        for output in data[i]['outputs']:
            vv = OutputPort(b,output + re.findall(r'_P\d+',i)[0])
            list_of_outputs.append(vv)
        list_of_to_file.append(b.write_block_w_port())
        list_of_block.append(b)
    
    links = {}
    i = 0
    for b in list_of_block:
        ports_b = [re.sub(r'_P\d+$', "", port.name) for port in b.get_input_ports()]
        for bb in list_of_block:
            if b != bb:
                ports_bb = [re.sub(r'_P\d+$', "", port.name) for port in bb.get_output_ports()]
                set_common = set(ports_b) & set(ports_bb)
                for e in set_common:
                    i += 1
                    links[f'link{i}']={'input': e + re.findall(r'_P\d+',b.name)[0],'output': e + re.findall(r'_P\d+',bb.name)[0]}
                    b.add_usage()
                    bb.add_usage()
    
    def delete_unlinked_block(list_of_block: list = list_of_block,list_of_to_file: list = list_of_to_file):
        for b in list_of_block:
            if b.usage == 0:
                chaine = b.name
                for to_file in list_of_to_file:
                    temp = re.findall(chaine, to_file)
                    if len(temp) >= 1 :
                        list_of_to_file.remove(to_file)
            

                
    fake_block = Block('a name')
    f = open('my_file.diag','w')
    f.write('blockdiag admin {\n')
    # delete_unlinked_block()
    for to_file in list_of_to_file:
        f.write(to_file)
    for link in links:
        f.write(Link(OutputPort(fake_block,links[link]['output']),InputPort(fake_block,links[link]['input']),link).write_link() + ';\n')
    f.write('}\n')

if __name__ == "__main__":
    main()
