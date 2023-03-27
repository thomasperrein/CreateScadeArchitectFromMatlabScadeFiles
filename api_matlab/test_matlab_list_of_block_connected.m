filepath = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP';
subsystem = '/BCM_COM_PROC_P20';

output = get_list_of_block_connected_with_port_associated(filepath,subsystem);

for i=1:length(output.from)
    display(output.from{1,i})
end

disp("END OF FROM")

for i=1:length(output.go)
    display(output.go{1,i})
end

disp("END OF GO")