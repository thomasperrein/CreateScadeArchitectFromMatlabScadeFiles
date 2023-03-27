function output = list_of_go(input, data_base_outport)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'DstBlock') && ~isempty(input(k).DstBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                type = input(k).Type;
                struct = {};
                name = getfullname(input(k).DstBlock);
                struct.name_of_port_associated = data_base_outport(type);
                if strcmp(get_param(name,'BlockType'), 'Goto')
                    struct.name_of_block = name;
                    output = [output, name];
                else
                    connectivity = get_param(name,'PortConnectivity');
                    if isstruct(connectivity)
                        output = [output, list_of_go(connectivity,data_base_outport)];
                    end
                end
            end
        end
    end
end