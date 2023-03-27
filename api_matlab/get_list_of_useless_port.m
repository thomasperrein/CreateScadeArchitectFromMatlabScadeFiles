function output = get_list_of_useless_port(input)
    output = cell(1,0);
    for k=1:length(input)
        if isfield(input(k),'DstBlock') && ~isempty(input(k).DstBlock)
            if isfield(input(k),'Type') && ~strcmp(input(k).Type,'enable')
                name = getfullname(input(k).DstBlock);
                if strcmp(get_param(name,'BlockType'), 'Terminator')
                    output = [output, get_param(name,'InputSignalNames')];
                end
            end
        end
    end
end