""" Script de test du package """

from scade_suite_file import *
import scade_env
import scade.model.suite, scade.model.project

PATH_2_5 = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P2_5\BCM_COM_PROC_P2_5.etp"
PATH_5 =  r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P5\BCM_COM_PROC_P5.etp"
PATH_20 = r"C:\TRAVAIL\BCM_WIP\CLEAN_VERSION\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\BCM_COM_PROC_P20\BCM_COM_PROC_P20.etp"

PATH_SESSION = r"C:\TRAVAIL\BCM_WIP\V1\F46_LGS_SW_WL\10_BCM_SW\BCM_CSCIs\01_COM\BCM_COM\BCM_COM_Design\02-SCADE_Models\MASTER\MASTER.etp"


def main(path):
    """ fonction principale """
    scade_file = ScadeFileSuite(path)
    return scade_file.data_of_interest()


def test():
    scade_env.load_project(PATH_SESSION)
    a = scade.model.suite.get_roots()
    b=a[0].unload()
    c=a[0].load2(PATH_2_5)
    a[0].unload()
    d=a[0].load2(PATH_5)
    carre = 0

if __name__=="__main__":
    test()
    

