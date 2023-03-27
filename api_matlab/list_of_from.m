function output = list_of_from(input,data_base_inport)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'SrcBlock') && ~isempty(input(k).SrcBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                type = input(k).Type;
                struct = {};
                struct.name_of_port_associated = data_base_inport(type);
                name = getfullname(input(k).SrcBlock);
                if strcmp(get_param(name,'BlockType'), 'From')
                    struct.name_of_block = name;
                    output = [output, struct];
                else
                    connectivity = get_param(name,'PortConnectivity');
                    if isstruct(connectivity)
                        output = [output, list_of_from(connectivity,data_base_inport)];
                    end
                end
            end
        end
    end
end