function output = list_of_from(input,data_base_inport, name_of_port)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'SrcBlock') && ~isempty(input(k).SrcBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                type = input(k).Type;
                struct = {};
                if strcmp(name_of_port,'')
                    struct.name_of_port_associated = data_base_inport(type);
                else
                    struct.name_of_port_associated = name_of_port;
                end
                name = getfullname(input(k).SrcBlock);
                if strcmp(get_param(name,'BlockType'), 'From') | strcmp(get_param(name,'BlockType'), 'Constant') | strcmp(get_param(name,'BlockType'), 'Ground')
                    struct.name_of_block = name;
                    output = [output, struct];
                else
                    connectivity = get_param(name,'PortConnectivity');
                    if isstruct(connectivity)
                        name_of_port_rec = data_base_inport(type);
                        output = [output, list_of_from(connectivity,data_base_inport,name_of_port_rec)];
                    end
                end
            end
        end
    end
end