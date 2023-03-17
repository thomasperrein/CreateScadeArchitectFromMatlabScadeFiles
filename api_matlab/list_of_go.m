function output = list_of_go(input)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'DstBlock') && ~isempty(input(k).DstBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                name = getfullname(input(k).DstBlock);
                if strcmp(get_param(name,'BlockType'), 'Goto')
                    output = [output, name];
                else
                    connectivity = get_param(name,'PortConnectivity');
                    if isstruct(connectivity)
                        output = [output, list_of_go(connectivity)];
                    end
                end
            end
        end
    end
end