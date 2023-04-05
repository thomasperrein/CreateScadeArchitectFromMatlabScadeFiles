#coding: utf-8
"""
Main programm to test firstly
"""
from archi import *
import re 
import pandas as pd

PATH_SESSION_SCADE = r"C:\TRAVAIL\BCM_WIP\V2\BCM_Design_S0B_MEX4.5\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\MASTER\MASTER.etp"
styleCSS_block = {
        'color': 'orange',
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
PATH_SIMULINK_MODEL = r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\F46_WBCS_Stub_BCM_AS_expurge'
PATH_API_MATLAB = r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]
PATH_FILEPATH = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP'
FILEPATHS_LISTS = ['F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P2_5/BCM_COM_PROC_P2_5',
                    'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P5/BCM_COM_PROC_P5',
                    'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P20/BCM_COM_PROC_P20'
                    ]

def main():
    """ main programm """
    archi_empty = archi.ARCHIFile('',[],[])
    archi_afterscade,_,__ = archi_empty.enrich_archi_with_scade(PATH_SESSION_SCADE,styleCSS_block,styleCSS_port,styleCSS_link)
    blocks_of_scade = archi_afterscade.blocks
    dic = {}
    for block in blocks_of_scade:
        dic[block.name] = {'inport': set(),'outport' : set()}
        for inport in block.get_input_ports():
            dic[block.name]['inport'].add(re.sub('_' + block.name,'',inport.name))
        for outport in block.get_output_ports():
            dic[block.name]['outport'].add(re.sub('_' + block.name,'',outport.name))

    archi_empty_2 = archi.ARCHIFile('',[],[])
    archi_aftermatlab,_,__ = archi_empty_2.enrich_archi_with_matlab2(PATH_SIMULINK_MODEL, FILEPATHS_LISTS, PATH_API_MATLAB, styleCSS_block,styleCSS_port,styleCSS_link)
    blocks_of_matlab = archi_aftermatlab.blocks
    dic2 = {}
    for block in blocks_of_matlab:
        dic2[block.name] = {'inport': set(),'outport' : set()}
        for inport in block.get_input_ports():
            dic2[block.name]['inport'].add(re.sub('_' + block.name,'',inport.name))
        for outport in block.get_output_ports():
            dic2[block.name]['outport'].add(re.sub('_' + block.name,'',outport.name))

    block_of_interest = ['BCM_COM_PROC_P20', 'BCM_COM_PROC_P2_5', 'BCM_COM_PROC_P5']
    dict_panda = {}
    for block in block_of_interest:
        dict_panda[f'{block} symmetric difference set of input'] = []
        for el in dic2[block]['inport'].symmetric_difference(dic[block]['inport']):
           dict_panda[f'{block} symmetric difference set of input'].append(el)
        dict_panda[f'{block} symmetric difference set of output'] = []
        for el in dic2[block]['outport'].symmetric_difference(dic[block]['outport']):
            dict_panda[f'{block} symmetric difference set of output'].append(el)
        dict_panda[f'{block} ports which are output in scade and input in matlab'] = []
        for el in dic[block]['outport'].intersection(dic2[block]['inport']):
            dict_panda[f'{block} ports which are output in scade and input in matlab'].append(el)
        dict_panda[f'{block} input ports that are in scade and not in matlab'] = []
        for el in dic[block]['inport'].difference(dic2[block]['inport']):
            dict_panda[f'{block} input ports that are in scade and not in matlab'].append(el)
        dict_panda[f'{block} input ports that are in matlab and not in scade'] = []
        for el in dic2[block]['inport'].difference(dic[block]['inport']):
            dict_panda[f'{block} input ports that are in matlab and not in scade'].append(el)
        dict_panda[f'{block} output ports that are in scade and not in matlab'] = []
        for el in dic[block]['outport'].difference(dic2[block]['outport']):
            dict_panda[f'{block} output ports that are in scade and not in matlab'].append(el)
        dict_panda[f'{block} output ports that are in matlab and not in scade'] = []
        for el in dic2[block]['outport'].difference(dic[block]['outport']):
            dict_panda[f'{block} output ports that are in matlab and not in scade'].append(el)
        df = pd.DataFrame({k: pd.Series(v) for k, v in dict_panda.items()})
        print(df)
        df.to_csv(f'pat_case_{block}.csv', index=False)





if __name__ == "__main__":
    main()
