import path_gestion
import scade_env
import scade.model.suite, scade.model.project

scade_env.load_project(r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P5\BCM_COM_PROC_P5.etp")

for item in scade.model.suite.get_roots():
    for node in item.model.nodes:
        print(f'name of the node in project : {node.name}')
        for output in node.outputs:
            print(f'in the node {node.name} we can find the output : {output.name}')
        for input in node.inputs:
            print(f'in the node {node.name} we can find the input : {input.name}')
