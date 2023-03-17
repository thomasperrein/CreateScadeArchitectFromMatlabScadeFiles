function output = list_of_from(input)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'SrcBlock') && ~isempty(input(k).SrcBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                name = getfullname(input(k).SrcBlock);
                if strcmp(get_param(name,'BlockType'), 'From')
                    output = [output, name];
                else
                    connectivity = get_param(name,'PortConnectivity');
                    if isstruct(connectivity)
                        output = [output, list_of_from(connectivity)];
                    end
                end
            end
        end
    end
end