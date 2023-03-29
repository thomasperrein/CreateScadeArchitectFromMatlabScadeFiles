"""
Main programm to test firstly
"""
import api_scade.scade_suite_file as sc
from model.block_port_link import Block, InputPort, OutputPort, Link
import scade_env
import scade.model.suite, scade.model.project
from archi import *
import diag.diag as diag

import re



def enrich_archi_with_scade(COLOR:list, PATH_SESSION_SCADE:str, archi_object:archi.ARCHIFile):
    """ main programm """
    styleCSS_block = {
        'shape' : 'box'
    }
    styleCSS_port = {
        'color' : 'white',
        'icon' : "'static/input_output.png'",
        'shape' : 'box'
    }
    styleCSS_link = {
        'color' : 'black',
        'dir' : 'forward'
    }
    list_of_to_file = []
    list_of_inputs = []
    list_of_outputs = []
    list_of_block = []
    list_of_links = []

    scade_env.load_project(PATH_SESSION_SCADE)
    a = scade.model.suite.get_roots()[0]
    scade_object = sc.ScadeFileSuite(a)
    # data = scade_object.data_of_interest()
    data = scade_object.data_of_nodes()

    for i,color in zip(data,COLOR):
        b = Block(i,color,**styleCSS_block)
        for input in data[i]['inputs']:
            v = InputPort(b,input + re.findall(r'_P\d+',i)[0],**styleCSS_port)
            list_of_inputs.append(v)
        for output in data[i]['outputs']:
            vv = OutputPort(b,output + re.findall(r'_P\d+',i)[0],**styleCSS_port)
            list_of_outputs.append(vv)
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
    for link in links:
        list_of_links.append(Link(OutputPort(fake_block,links[link]['output']),InputPort(fake_block,links[link]['input']),link,**styleCSS_link))
    
    diag_object = diag.DIAGFile('diag after scade', list_of_block, list_of_links)
    diag_object.write_diag_file('my_file.diag')

    for block in list_of_block:
        archi_object.add_block(block)
    for link in list_of_links:
        archi_object.add_link(link)
    archi_object.write_archi_file('my_file.archi')
    
    return(archi_object)

if __name__ == "__main__":
    enrich_archi_with_scade()
