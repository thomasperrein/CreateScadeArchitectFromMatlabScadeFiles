filepath = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP';
subsystem = 'BCM_COM_PROC_P20';

output = get_list_of_useless_port(filepath,subsystem);

for i=1:length(output)
    disp(output{1,i})
end

disp("END OF USELESS PORT")
