function output = get_list_of_block_connected_with_port_associated(filepath,subsystem)
    output.from = cell(1,0);
    output.go = cell(1,0);
    true_path = strcat(filepath,'/',subsystem);
    input_port = find_system(true_path,'SearchDepth',1,'BlockType','Inport'); % we search here all the inport block inside the subsystem
    data_base_inport = containers.Map; % declaration of data base inport which is a dictionary where key = object port and value is name of port

    for k=1:numel(input_port)
        data_base_inport(get_param(input_port{k,1},'Port')) = get_param(input_port{k,1},'PortName'); % to identify a port object with his name 
    end
    
    from_list = list_of_from(get_param(true_path,'PortConnectivity'), data_base_inport, '');
    for k=1:length(from_list)
        new_struct = {};
        if strcmp(get_param(from_list{1,k}.name_of_block,'BlockType'),'From')
            temp = get_param(from_list{1,k}.name_of_block,'GotoTag');
            name = find_system(filepath,'GotoTag',temp,'BlockType','Goto');
            structure = get_param(name,'PortConnectivity');
            new_struct.name = getfullname(structure{1,1}.SrcBlock);
            new_struct.port_associated = from_list{1,k}.name_of_port_associated;
        else
            new_struct.name = from_list{1,k}.name_of_block;
            new_struct.port_associated = from_list{1,k}.name_of_port_associated;
        end
        output.from = cat(2,output.from,new_struct);
    end
    
    output_port = find_system(true_path,'SearchDepth',1,'BlockType','Outport');
    data_base_outport = containers.Map;

    for k=1:numel(output_port)
        data_base_outport(get_param(output_port{k,1},'Port')) = get_param(output_port{k,1},'PortName');
    end
    go_list = list_of_go(get_param(true_path,'PortConnectivity'),data_base_outport);
    for k=1:length(go_list)
        new_struct = {};
        temp = get_param(go_list{1,k}.name_of_block,'GotoTag');
        name = find_system(filepath,'GotoTag',temp,'BlockType','From');
        structure = get_param(name,'PortConnectivity');
        if strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'UnitDelay')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            new_struct.name = new_name;
            new_struct.port_associated = go_list{1,k}.name_of_port_associated;
            output.go = cat(2,output.go,new_struct);
        elseif strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'Demux')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            new_struct.name = new_name;
            new_struct.port_associated = go_list{1,k}.name_of_port_associated;
            output.go = cat(2,output.go,new_struct);
        elseif strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'DataTypeConversion')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            new_struct.name = new_name;
            new_struct.port_associated = go_list{1,k}.name_of_port_associated;
            output.go = cat(2,output.go,new_struct);
        else
            new_struct.name = getfullname(structure{1,1}.DstBlock);
            new_struct.port_associated = go_list{1,k}.name_of_port_associated;
            output.go = cat(2,output.go,new_struct);
        end
    end
end