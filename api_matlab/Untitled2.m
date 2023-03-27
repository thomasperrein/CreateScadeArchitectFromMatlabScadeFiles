filepath = 'F46_WBCS_Stub_BCM_AS_expurge/AVIONICS/Brake_Control_Module_Side_A/BCSA Controller CP';
subsystem = '/BCM_COM_PROC_P20';

a = get_param(strcat(filepath,subsystem),'PortConnectivity');

input_port = find_system(strcat(filepath,subsystem),'SearchDepth',1,'BlockType','Inport');
data_base_inport = containers.Map;

for k=1:numel(input_port)
    data_base_inport(get_param(input_port{k,1},'Port')) = get_param(input_port{k,1},'PortName');
end

output_port = find_system(strcat(filepath,subsystem),'SearchDepth',1,'BlockType','Outport');

output = cell(1,0);
for k=1:length(a)
    if isfield(a(k),'SrcBlock') && ~isempty(a(k).SrcBlock)
        if isfield(a(k),'Type') && ~strcmp(a(k).Type,'enable')
            type = a(k).Type;
            struct = {};
            name_of_block = getfullname(a(k).SrcBlock);
            struct.name_of_block = name_of_block;
            struct.name_of_port_associated = data_base_inport(type);
            output = [output, struct];
        end
    end
end