#coding: utf-8
"""
Main programm to test firstly
"""
import api_scade.scade_suite_file as sc
from model.block_port_link import Block, InputPort, OutputPort, Link


PATH_2_5 = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P2_5\BCM_COM_PROC_P2_5.etp"
PATH_5 =  r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P5\BCM_COM_PROC_P5.etp"
PATH_20 = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P20\BCM_COM_PROC_P20.etp"
COLOR = ["blue","red","orange"]

PATH_SESSION = r"C:\TRAVAIL\BCM_WIP\V1\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\MASTER\MASTER.etp"


def main():
    """ main programm """
    list_of_to_file = []
    list_of_inputs = []
    list_of_outputs = []
    list_of_block = []
    
    scade_object = sc.ScadeFileSuite(PATH_SESSION)
    data = scade_object.data_of_interest()

    for i,color in zip(data,COLOR):
        for j in data[i]:
            b = Block(j,color)
            for input in data[i][j]['inputs']:
                v = InputPort(b,input + '_' + j[:3])
                list_of_inputs.append(v)
            for output in data[i][j]['outputs']:
                vv = OutputPort(b,output + '_' + j[:3])
                list_of_outputs.append(vv)
            list_of_to_file.append(b.write_block_w_port())
            list_of_block.append(b)


    
    links = {}
    i = 0
    for b in list_of_block:
        ports_b = [port.name[:-4] for port in b.get_input_ports()]
        for bb in list_of_block:
            if b != bb:
                ports_bb = [port.name[:-4] for port in bb.get_output_ports()]
                set_common = set(ports_b) & set(ports_bb)
                for e in set_common:
                    i += 1
                    links[f'link{i}']={'input': locals()[e + '_' + b.name[:3]],'output': locals()[e + '_' + bb.name[:3]]}

    # set_of_input = set()
    # set_of_output = set()

    # for i in data:
    #     for j in data[i]:
    #         for input in data[i][j]['inputs']:
                

    f = open('my_file.diag','w')
    f.write('blockdiag admin {\n')
    for to_file in list_of_to_file:
        f.write(to_file)
    for link in links:
        f.write(Link(links[link]['output'],links[link]['input'],link).write_link())
    f.write('}\n')

if __name__ == "__main__":
    main()
