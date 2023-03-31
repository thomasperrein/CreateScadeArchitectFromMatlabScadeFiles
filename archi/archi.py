""" Definition of ARCHI File which is derived of XML file """
from model.block_port_link import Block, Link, InputPort, OutputPort
from typing import List
from file.file import File
from diag.diag import DIAGFile
import copy

class ARCHIFile(File):
    """ Archi file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        super().__init__(name, blocks, links)
        
        
    def write_archi_file(self, path:str) -> None:
        """ write the archi file corresponding to the object """
        f = open(path, 'w')
        f.write('<archi>\n')
        f.write(self.write_block())
        f.write(self.write_link())
        f.write('</archi>\n')
        f.close()
        print(f"File {self.name} written at {path}")


    def write_block(self) -> str:
        """ return the string corresponding to the block (balise etc.) """
        text = ""
        for block in self.blocks:
            temp = block.write_attributes(InARCHIFile = True)
            text = text + f"""\t<block {temp}>\n"""
            for input in block.get_input_ports():
                temp = input.write_attributes(InARCHIFile = True)
                text = text + f"""\t\t<input {temp}/>\n"""
            for output in block.get_output_ports():
                temp = output.write_attributes(InARCHIFile = True)
                text = text + f"""\t\t<output {temp}/>\n"""
            text = text + f"""\t</block>\n"""
        return text

    def write_link(self) -> str:
        """ return the string corresponding to the link (balise etc.) """
        text = ""
        for link in self.links:
            temp = link.write_attributes(InARCHIFile= True)
            if link.dir == None:
                text = text + f"""\t<link {temp}>\n"""
            else:
                text = text + f"""\t<link {temp} dir = "{link.dir}">\n"""
            text = text + f"""\t\t<input name = "{link.input_port.name}"/>\n"""
            text = text + f"""\t\t<output name = "{link.output_port.name}"/>\n"""
            text = text + f"""\t</link>\n"""
        return text


    def enrich_blocks(self, new_blocks: List[Block]):
        """ mix the previous attributes blocks with new blocks by adding new ports to already declared blocks and new blocks with their ports to the list of blocks """
        new_self_blocks = copy.deepcopy(self.blocks)
        correspondance_name_block = {block.name : block for block in new_self_blocks}
        for block in new_blocks: #For all the new blocks found
            if block.name in correspondance_name_block.keys(): #If it already exists => check if all the ports are the same
                name_port = [port.name for port in correspondance_name_block[block.name].get_all_ports()]
                for port in block.get_all_ports(): #So for all ports in the new block found
                    if not(port.name in name_port): #if it is not in the ports name already given
                        attrib = {key: value for key, value in port.__dict__.items() if not key.startswith("__")} # We add it by retrieve his attribute
                        attrib['block'] = correspondance_name_block[block.name] #change the block associated
                        if isinstance(port, InputPort):
                            InputPort(**attrib) #create a new inport with the same attribute except the block, which will be the one attached to the archi file
                        elif isinstance(port, OutputPort):
                            OutputPort(**attrib)
                        else:
                            continue  
                        # correspondance_name_block[block.name].ports.append(port)
            else:
                new_self_blocks.append(copy.copy(block))
        self.blocks = new_self_blocks


    def enrich_links(self, new_links: List[Link]):
        """ add new links if they haven't been already declared) """
        new_self_links = copy.deepcopy(self.links)
        link_to_add = []
        for link_new in new_links:
            for link_file in new_self_links:
                if (link_new.input_port.name == link_file.input_port.name) & (link_new.output_port.name == link_file.output_port.name):
                    continue
                else:
                    attrib = {key: value for key, value in link_new.__dict__.items() if not key.startswith("__")} # We add it by retrieve his attribute
                    link_to_add.append(Link(**attrib))
        self.links = new_self_links + link_to_add
    

    def enrich_link_block(self, new_blocks: List[Block], new_links: List[Link]):
        """ enrich with oth functions enrich link and enrich block """
        self.enrich_blocks(new_blocks)
        self.enrich_links(new_links)
    
        
    def convert_to_diag(self) -> DIAGFile:
        new_blocks = copy.copy(self.blocks)
        new_links = copy.copy(self.links)
        return(DIAGFile(self.name, new_blocks, new_links))