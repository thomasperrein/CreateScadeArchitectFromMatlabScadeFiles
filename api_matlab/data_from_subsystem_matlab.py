import os
import matlab.engine as matlab_engine


def data_from_subsystem_matlab(path_simulinkmodel:str, filename:str, subsystem:str, path_of_matlab_functions:str):
    path = os.getcwd()
    os.chdir(path_of_matlab_functions)
    eng = matlab_engine.start_matlab()
    eng.open_system(path_simulinkmodel,nargout = 0)
    eng.addpath(path_of_matlab_functions, nargout=0)
    output1 = eng.get_list_of_block_connected_with_port_associated(filename,subsystem)
    output2 = eng.get_list_of_useless_port(filename,subsystem)
    eng.quit()
    os.chdir(path)
    return(output1,output2)

if __name__ == "__main__":
    print(data_from_subsystem_matlab(r'test_package/MATLAB_TEST','MATLAB_TEST/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP','BCM_COM_PROC_P5', r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1])) 