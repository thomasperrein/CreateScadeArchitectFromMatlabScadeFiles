import sys
import os

sys.path.append(r'C:\Program Files\MATLAB\R2019b\extern\engines\python\dist\matlab')

import matlab.engine as matlab_engine

os.chdir(r'C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab')
# Démarrer l'API MATLAB
eng = matlab_engine.start_matlab()

# eng.evalc('prj = openProject('+r"C:\Users\fx622208\MATLAB\Projects\test_api\Test_api.prj"+');')

eng.open_system("../F46_WBCS_Stub_BCM_AS_expurge",nargout = 0)

# ModelName = 'fmu'
# eng.sys_print(ModelName, nargout=0)

a = eng.get_list_of_block_connected('F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP','/BCM_COM_PROC_P2_5')
# print(a['Inport'])
print(a)
eng.quit()