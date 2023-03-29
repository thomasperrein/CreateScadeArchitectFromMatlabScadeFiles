#coding: utf-8
"""
Main programm to test firstly
"""
import api_scade.scade_suite_file as sc
from model.block_port_link import Block, InputPort, OutputPort, Link
from archi import *
import scade_env
import scade.model.suite, scade.model.project
import enrich_archi_with_matlab as enrich_matlab
import enrich_archi_with_scade as enrich_scade


import re

COLOR = ["blue","red","orange","green"]

PATH_ARCHI_FILE = r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\test.archi'
PATH_SESSION_SCADE = r"C:\TRAVAIL\BCM_WIP\V1\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\MASTER\MASTER.etp"

PATH_SIMULINK_MODEL = r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\F46_WBCS_Stub_BCM_AS_expurge'
PATH_API_MATLAB = r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]
PATH_FILEPATH = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP'
SUBSYSTEM_LISTS = ['BCM_COM_PROC_P2_5','BCM_COM_PROC_P5','BCM_COM_PROC_P20']


def main():
    """ main programm """
    archi_empty = archi.ARCHIFile('',[],[])
    archi_afterscade = enrich_scade.enrich_archi_with_scade(COLOR,PATH_SESSION_SCADE, archi_empty)
    archi_aftermatlab = enrich_matlab.enrich_archi_with_matlab(PATH_SIMULINK_MODEL, PATH_FILEPATH, SUBSYSTEM_LISTS, PATH_API_MATLAB, archi_afterscade)

if __name__ == "__main__":
    main()
