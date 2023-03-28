"""
Main programm to test firstly
"""
from model.block_port_link import Block, InputPort, OutputPort, Link
from archi import *
from api_matlab import data_from_subsystem_matlab

import re



def enrich_archi_with_matlab(path_simulink:str, filepath:str, subsystems:list, path_api:str, archi_object:archi.ARCHIFile):
    """ main programm """
    data_matlab = data_from_subsystem_matlab.data_from_several_subsystem_matlab(path_simulink,filepath,subsystems,path_api)
    for data in data_matlab:
        name_of_block = data
        output = data_matlab[data]
    return(archi_object)

if __name__ == "__main__":
    enrich_archi_with_matlab()
