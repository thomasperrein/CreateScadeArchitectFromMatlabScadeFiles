function output = get_list_of_block_connected(filepath,subsystem)
    output.from = cell(1,0);
    output.go = cell(1,0);
    from_list = list_of_from(get_param(strcat(filepath,subsystem),'PortConnectivity'));
    go_list = list_of_go(get_param(strcat(filepath,subsystem),'PortConnectivity'));
    for k=1:length(from_list)
        temp = get_param(from_list{1,k},'GotoTag');
        name = find_system(filepath,'GotoTag',temp,'BlockType','Goto');
        structure = get_param(name,'PortConnectivity');
        output.from = cat(2,output.from,getfullname(structure{1,1}.SrcBlock));
    end
    for k=1:length(go_list)
        temp = get_param(go_list{1,k},'GotoTag');
        name = find_system(filepath,'GotoTag',temp,'BlockType','From');
        structure = get_param(name,'PortConnectivity');
        if strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'UnitDelay')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            output.go = cat(2,output.go,new_name);
        elseif strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'Demux')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            output.go = cat(2,output.go,new_name);
        elseif strcmp(get_param(getfullname(structure{1,1}.DstBlock),'BlockType'),'DataTypeConversion')
            temp2 = get_param(getfullname(structure{1,1}.DstBlock),'Portconnectivity');
            new_name = getfullname(temp2(2).DstBlock);
            output.go = cat(2,output.go,new_name);
        else
            output.go = cat(2,output.go,getfullname(structure{1,1}.DstBlock));
        end
    end
end