function output = get_list_of_block_connected_corrected(filepath)
    input_port_1 = find_system(filepath,'SearchDepth',1,'BlockType','Inport'); % we search here all the inport block inside the subsystem
    data_base_inport_1 = containers.Map; % declaration of data base inport which is a dictionary where key = object port and value is name of port
    output_port_1 = find_system(filepath,'SearchDepth',1,'BlockType','Outport');
    data_base_outport_1 = containers.Map;
    obj = get_param(filepath, 'PortConnectivity');



    input_port = find_system(get_param(filepath,'Parent'),'SearchDepth',1,'BlockType','Inport'); % we search here all the inport block inside the subsystem
    data_base_inport = containers.Map; % declaration of data base inport which is a dictionary where key = object port and value is name of port
    output_port = find_system(get_param(filepath,'Parent'),'SearchDepth',1,'BlockType','Outport');
    data_base_outport = containers.Map;
    obj2 = get_param(get_param(filepath,'Parent'), 'PortConnectivity');

    output = {};
    e = cell(0,0);

    for j=1:numel(input_port)
        data_base_inport(get_param(input_port{j,1},'PortName')) = get_param(input_port{j,1},'Port') ; % to identify a port object with his name 
    end


    for k=1:numel(input_port_1)
        data_base_inport_1(get_param(input_port_1{k,1},'Port')) = get_param(input_port_1{k,1},'PortName'); % to identify a port object with his name 
    end

    for j=1:numel(output_port)
        data_base_outport(get_param(output_port{j,1},'PortName')) = get_param(output_port{j,1},'Port') ; % to identify a port object with his name 
    end


    for k=1:numel(output_port_1)
        data_base_outport_1(get_param(output_port_1{k,1},'Port')) = get_param(output_port_1{k,1},'PortName'); % to identify a port object with his name 
    end

    index = 1 ;

    for k=1:numel(obj)
        a = obj(k).SrcBlock;
        b = cell(1,0);
        if strcmp(get_param(a,'BlockType'),'Inport')
            b{1,1} = get_param(a,'Name');
            type = data_base_inport(b{1,1});
            e{end+1,1}.name_of_port_associated = input_port_1{index,1};
            for j=1:length(obj2)
                if strcmp(obj2(j).Type, type) && isempty(obj2(j).DstBlock)
                    if strcmp(get_param(obj2(j).SrcBlock,'BlockType'),'Selector') | strcmp(get_param(obj2(j).SrcBlock,'BlockType'),'Delay') | strcmp(get_param(obj2(j).SrcBlock,'BlockType'),'UnitDelay')
                        temp_port_co = get_param(obj2(j).SrcBlock,'PortConnectivity');
                        for num=1:numel(temp_port_co)
                            if isempty(temp_port_co(num).DstBlock)
                                if strcmp(get_param(temp_port_co(num).SrcBlock,'BlockType'),'From')
                                    temp = get_param(temp_port_co(num).SrcBlock,'GotoTag');
                                    name = find_system(get_param(get_param(filepath,'Parent'),'Parent'),'GotoTag',temp,'BlockType','Goto');
                                    structure = get_param(name,'PortConnectivity');
                                    e{end,1}.block = {get_param(structure{1,1}.SrcBlock,'Name')};
                                else
                                    e{end,1}.block = {get_param(temp_port_co(num).SrcBlock,'Name')};
                                end
                            end
                        end
                    elseif strcmp(get_param(obj2(j).SrcBlock,'BlockType'),'From')
                        temp = get_param(obj2(j).SrcBlock,'GotoTag');
                        name = find_system(get_param(get_param(filepath,'Parent'),'Parent'),'GotoTag',temp,'BlockType','Goto');
                        structure = get_param(name,'PortConnectivity');
                        e{end,1}.block = {get_param(structure{1,1}.SrcBlock,'Name')};
                    else
                        e{end,1}.block = {get_param(obj2(j).SrcBlock,'Name')};
                    end
                end
            end
            index = index + 1;
        elseif strcmp(get_param(a,'BlockType'),'Mux')
            port_connectivity_mux = get_param(a,'PortConnectivity');
            i = 1;
            for el=1:numel(port_connectivity_mux)
                if isempty(port_connectivity_mux(el).DstBlock)
                    b{i,1} = get_param(port_connectivity_mux(el).SrcBlock,'Name');
                    type = data_base_inport(b{i,1});
                    i = i + 1;
                    e{end+1,1}.name_of_port_associated = input_port_1{index,1};
                    for j=1:length(obj2)
                        if strcmp(obj2(j).Type, type) && isempty(obj2(j).DstBlock)
                            to_comp = get_param(obj2(j).SrcBlock,'BlockType');
                            if strcmp(to_comp,'Delay')
                                temp_port_co = get_param(obj2(j).SrcBlock,'PortConnectivity');
                                for num=1:numel(temp_port_co)
                                    if isempty(temp_port_co(num).DstBlock)
                                        e{end,1}.block = {get_param(temp_port_co(num).SrcBlock,'Name')};
                                    end
                                end
                            elseif strcmp(to_comp,'From')
                                temp = get_param(obj2(j).SrcBlock,'GotoTag');
                                name = find_system(get_param(get_param(filepath,'Parent'),'Parent'),'GotoTag',temp,'BlockType','Goto');
                                structure = get_param(name,'PortConnectivity');
                                e{end,1}.block = {get_param(structure{1,1}.SrcBlock,'Name')};
                            else
                                e{end,1}.block = {get_param(obj2(j).SrcBlock,'Name')};
                            end
                        end
                    end
                end
            end
            index = index + 1;
        end
    end
    output.from = e;

    e = cell(0,0);
    index = 1;

    for k=1:numel(obj)
        a = obj(k).DstBlock;
        b = cell(1,0);
        if strcmp(get_param(a,'BlockType'),'Outport')
            b{1,1} = get_param(a,'Name');
            type = data_base_outport(b{1,1});
            e{end+1,1}.name_of_port_associated = output_port_1{index,1};
            for j=1:length(obj2)
                if strcmp(obj2(j).Type, type) && isempty(obj2(j).SrcBlock)
                    if strcmp(get_param(obj2(j).DstBlock,'BlockType'),'Selector') | strcmp(get_param(obj2(j).DstBlock,'BlockType'),'Delay') | strcmp(get_param(obj2(j).DstBlock,'BlockType'),'UnitDelay')
                        temp_port_co = get_param(obj2(j).DstBlock,'PortConnectivity');
                        for num=1:numel(temp_port_co)
                            if isempty(temp_port_co(num).SrcBlock)
                                if strcmp(get_param(temp_port_co(num).DstBlock,'BlockType'),'Goto')
                                    temp = get_param(temp_port_co(num).DstBlock,'GotoTag');
                                    name = find_system(get_param(get_param(filepath,'Parent'),'Parent'),'GotoTag',temp,'BlockType','From');
                                    structure = get_param(name,'PortConnectivity');
                                    e{end,1}.block = {get_param(structure{1,1}.DstBlock,'Name')};
                                else
                                    e{end,1}.block = {get_param(temp_port_co(num).DstBlock,'Name')};
                                end
                            end
                        end
                    elseif strcmp(get_param(obj2(j).DstBlock,'BlockType'),'Goto')
                        temp = get_param(obj2(j).DstBlock,'GotoTag');
                        name = find_system(get_param(get_param(filepath,'Parent'),'Parent'),'GotoTag',temp,'BlockType','From');
                        one_cell = cell(numel(name),1);
                        for el_name=1:numel(name)
                            structure = {get_param(name{el_name,1},'PortConnectivity')};
                            if strcmp(get_param(structure{1,1}.DstBlock,'BlockType'),'UnitDelay') | strcmp(get_param(structure{1,1}.DstBlock,'BlockType'),'Delay') | strcmp(get_param(structure{1,1}.DstBlock,'BlockType'),'Demux')
                                tempo = get_param(structure{1,1}.DstBlock,'PortConnectivity');
                                for m=1:numel(tempo)
                                    if isempty(tempo(m).SrcBlock)
                                        one_cell{el_name,1} = get_param(tempo(m).DstBlock,'Name');
                                    end
                                end
                            else
                                one_cell{el_name,1} = get_param(structure{1,1}.DstBlock,'Name');
                            end
                        end
                        e{end,1}.block = one_cell;
                    else
                        e{end,1}.block = {get_param(obj2(j).DstBlock,'Name')};
                    end
                end
            end
            index = index + 1;
        end
    end

    output.go = e;
