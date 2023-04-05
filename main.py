#coding: utf-8
"""
Main programm to test firstly
"""
from archi import *

PATH_ARCHI_FILE = r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\test.archi'
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
SUBSYSTEM_LISTS = ['BCM_COM_PROC_P2_5','BCM_COM_PROC_P5','BCM_COM_PROC_P20']
FILEPATHS_LISTS = ['F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P2_5/BCM_COM_PROC_P2_5',
                    'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P5/BCM_COM_PROC_P5',
                    'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP/BCM_COM_PROC_P20/BCM_COM_PROC_P20'
                    ]

def main():
    """ main programm """
    archi_empty = archi.ARCHIFile('',[],[])
    archi_afterscade,_,__ = archi_empty.enrich_archi_with_scade(PATH_SESSION_SCADE,styleCSS_block,styleCSS_port,styleCSS_link)
    assert archi_afterscade.filecmp(archi_empty)
    # archi_file, diag_file,__= archi_empty.enrich_archi_with_matlab(PATH_SIMULINK_MODEL, PATH_FILEPATH, SUBSYSTEM_LISTS, PATH_API_MATLAB,styleCSS_block,styleCSS_port,styleCSS_link)
    archi_file, diag_file,__= archi_empty.enrich_archi_with_matlab2(PATH_SIMULINK_MODEL, FILEPATHS_LISTS, PATH_API_MATLAB, styleCSS_block,styleCSS_port,styleCSS_link)
    archi_empty.write_archi_file("archi_file_after_fusion.archi")
    diag_file.adapt_colors_w_clustering()
    diag_file.write_diag_file("diag_file_after_fusion.diag")


def scade():
    """ scade """
    archi_empty_2 = archi.ARCHIFile('',[],[])
    archi_afterscade, diag_afterscade,_ = archi_empty_2.enrich_archi_with_scade(PATH_SESSION_SCADE,styleCSS_block,styleCSS_port,styleCSS_link)
    archi_empty_2.write_archi_file('file_scade.archi')
    diag_afterscade.adapt_colors_w_clustering()
    diag_afterscade.write_diag_file('my_file.diag')


def matlab():
    """ matlab """
    archi_empty_3 = archi.ARCHIFile('',[],[])
    archi_aftermatlab, diag_aftermatlab,_ = archi_empty_3.enrich_archi_with_matlab(PATH_SIMULINK_MODEL, PATH_FILEPATH, SUBSYSTEM_LISTS, PATH_API_MATLAB, styleCSS_block, styleCSS_port, styleCSS_link)
    archi_empty_3.write_archi_file('file_matlab.archi')
    diag_aftermatlab.adapt_colors_w_clustering()
    diag_aftermatlab.write_diag_file('my_file_2.diag')


def matlab2():
    """ matlab """
    archi_empty_3 = archi.ARCHIFile('',[],[])
    archi_aftermatlab, diag_aftermatlab,_ = archi_empty_3.enrich_archi_with_matlab2(PATH_SIMULINK_MODEL, FILEPATHS_LISTS, PATH_API_MATLAB, styleCSS_block,styleCSS_port,styleCSS_link)
    archi_empty_3.write_archi_file('file_matlab.archi')
    diag_aftermatlab.adapt_colors_w_clustering()
    diag_aftermatlab.write_diag_file('my_file_2.diag')


if __name__ == "__main__":
    main()
    # scade()
    # matlab()
    matlab2()
