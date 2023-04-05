import os
import matlab.engine as matlab_engine


def data_from_subsystem_matlab(path_simulinkmodel:str, filename:str, subsystem:str, path_of_matlab_functions:str):
    """ retrieve data from subsystem Matlab : bloc connected (with goto/from taken into account) and port associated
        retrieve also useless port for subsystem -> all the output ports that goes to a terminate block
    """
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


def data_from_several_subsystem_matlab(path_simulinkmodel:str, filename:str, subsystems:list, path_of_matlab_functions:str):
    """ optimize data_from_subsystem_matlab for several subsystem in a subsystem list of string """
    path = os.getcwd()
    output_list = {}
    os.chdir(path_of_matlab_functions)
    eng = matlab_engine.start_matlab()
    eng.open_system(path_simulinkmodel,nargout = 0)
    eng.addpath(path_of_matlab_functions, nargout=0)
    for subsystem in subsystems:
        # output1 = eng.get_list_of_block_connected_with_port_associated(filename+'/'+subsystem,subsystem)
        output1 = eng.get_list_of_block_connected_with_port_associated(filename,subsystem)
        output2 = eng.get_list_of_useless_port(filename,subsystem)
        output_list[subsystem] = (output1,output2)
    eng.quit()
    os.chdir(path)
    return(output_list)


def data_from_several_subsystem_matlab_corrected(path_simulinkmodel:str, filepaths:list, path_of_matlab_functions:str):
    path = os.getcwd()
    output_list = {}
    os.chdir(path_of_matlab_functions)
    eng = matlab_engine.start_matlab()
    eng.open_system(path_simulinkmodel,nargout = 0)
    eng.addpath(path_of_matlab_functions, nargout=0)
    for filepath in filepaths:
        # output1 = eng.get_list_of_block_connected_with_port_associated(filename+'/'+subsystem,subsystem)
        output1 = eng.get_list_of_block_connected_corrected(filepath)
        output_list[filepath] = (output1)
    eng.quit()
    os.chdir(path)
    return(output_list)


if __name__ == "__main__":
    SUBSYSTEM_LISTS = ['BCM_COM_PROC_P2_5','BCM_COM_PROC_P5','BCM_COM_PROC_P20']
    FILEPATHS_LIST = ['test_script/BCM_COM_PROC_P20/BCM_COM_PROC_P20']
    # print(data_from_subsystem_matlab(r'test_package/MATLAB_TEST','MATLAB_TEST/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP','BCM_COM_PROC_P5', r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]))
    # print(data_from_several_subsystem_matlab(r'test_package/MATLAB_TEST','MATLAB_TEST/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP', SUBSYSTEM_LISTS, r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]))
    print(data_from_several_subsystem_matlab_corrected(r'test_package/test_script', FILEPATHS_LIST, r"C:\TRAVAIL\GenerationModel\FindLinkBetweenNodesScade\api_matlab\ "[:-1]))