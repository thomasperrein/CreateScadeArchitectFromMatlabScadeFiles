""" Script de test du package """

from scade_suite_file import *

PATH_TEST  = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P5\BCM_COM_PROC_P5.etp"

def main(path):
    """ fonction principale """
    scade_file = ScadeFileSuite(path)
    return scade_file.data_of_interest()


if __name__=="__main__":
    data = main(PATH_TEST)
    print(data)
