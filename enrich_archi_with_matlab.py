"""
Main programm to test firstly
"""
from model.block_port_link import Block, InputPort, OutputPort, Link
from archi import *
from api_matlab import data_from_subsystem_matlab

import re



def enrich_archi_with_matlab(path_simulink:str, filepath:str, subsystems:list, path_api:str, archi_object:archi.ARCHIFile):
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

    correspondance_name_objet = {}

    data_matlab = data_from_subsystem_matlab.data_from_several_subsystem_matlab(path_simulink,filepath,subsystems,path_api)
    
    for data in data_matlab:
        b = Block(data,**styleCSS_block)
        correspondance_name_objet[data] = b
        list_of_block.append(b)
        for e in data_matlab[data][0]['from']:
            if e['name'].split('/')[-1].replace('\n',"").replace(' ','_') not in correspondance_name_objet:
                name_of_new_block = e['name'].split('/')[-1].replace('\n',"").replace(' ','_')
                new_block = Block(name_of_new_block,'blue',**styleCSS_block)
                list_of_block.append(new_block)
                correspondance_name_objet[name_of_new_block] = new_block
            new_block = correspondance_name_objet[e['name'].split('/')[-1].replace('\n',"").replace(' ','_')]
            vv = OutputPort(new_block, e['port_associated'] + '_' + e['name'].split('/')[-1].replace('\n',"").replace(' ','_'), **styleCSS_port)
            v = InputPort(b, e['port_associated'] + '_' + data, **styleCSS_port)
            link = Link(vv,v,'link',**styleCSS_link)
            list_of_links.append(link)
        for e in data_matlab[data][0]['go']:
            if e['name'].split('/')[-1].replace('\n',"").replace(' ','_') not in correspondance_name_objet:
                name_of_new_block = e['name'].split('/')[-1].replace('\n',"").replace(' ','_')
                new_block = Block(name_of_new_block,'blue',**styleCSS_block)
                list_of_block.append(new_block)
                correspondance_name_objet[name_of_new_block] = new_block
            new_block = correspondance_name_objet[e['name'].split('/')[-1].replace('\n',"").replace(' ','_')]
            vv = InputPort(new_block, e['port_associated'] + '_' + e['name'].split('/')[-1].replace('\n',"").replace(' ','_'), **styleCSS_port)
            v = OutputPort(b, e['port_associated'] + '_' + data, **styleCSS_port)
            link = Link(v,vv,'link',**styleCSS_link)
            list_of_links.append(link)

    print(data_matlab)

    for b in list_of_block:
        list_of_to_file.append(b.write_block_w_port())

    f = open('my_file_2.diag','w')
    f.write('blockdiag admin {\n')
    # delete_unlinked_block()
    for to_file in list_of_to_file:
        f.write(to_file)
    for link in list_of_links:
        f.write(link.write_link() + ';\n')
    f.write('}\n')

    name_of_archi_object = archi_object.name
    archi_object_after_matlab = archi.ARCHIFile(name_of_archi_object, list_of_block, list_of_links)
    return(archi_object_after_matlab)

if __name__ == "__main__":
    PATH_SIMULINK_MODEL = r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\F46_WBCS_Stub_BCM_AS_expurge'
    PATH_API_MATLAB = r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]
    PATH_FILEPATH = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP'
    SUBSYSTEM_LISTS = ['BCM_COM_PROC_P2_5','BCM_COM_PROC_P5','BCM_COM_PROC_P20']
    archi_empty = archi.ARCHIFile('',[],[])
    archi_aftermatlab = enrich_archi_with_matlab(PATH_SIMULINK_MODEL, PATH_FILEPATH, SUBSYSTEM_LISTS, PATH_API_MATLAB, archi_empty)
    print(archi_aftermatlab)