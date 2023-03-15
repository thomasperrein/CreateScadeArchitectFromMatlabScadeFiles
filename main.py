#coding: utf-8
"""
Main programm to test firstly
"""
import api_scade.scade_suite_file as sc
from model.block_port_link import Block, InputPort, OutputPort, Link

PATH = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P5\BCM_COM_PROC_P5.etp"

def main():
    """ main programm """
    scade_object = sc.ScadeFileSuite(PATH)
    data = scade_object.data_of_interest()

    list_of_to_file = []
    list_of_inputs = []
    list_of_outputs = []
    list_of_block = []

    for i in data:
        for j in data[i]:
            b = Block(j + '_' + i,"blue")
            for input in data[i][j]['inputs']:
                v = InputPort(b,input.name + '_' + j[:4])
                list_of_inputs.append(v)
            for output in data[i][j]['outputs']:
                vv = OutputPort(b,output.name + '_' + j[:4])
                list_of_outputs.append(vv)
            list_of_to_file.append(b.write_block_w_port())
            list_of_block.append(b)

    f = open('my_file.diag','w')
    f.write('blockdiag admin {\n')
    for to_file in list_of_to_file:
        f.write(to_file)
    f.write('}\n')

if __name__ == "__main__":
    main()
