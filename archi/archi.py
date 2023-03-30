""" Definition of ARCHI File which is derived of XML file """
from model.block_port_link import Block, Link
from typing import List
from file.file import File
from diag.diag import DIAGFile

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


    def enrich_blocks(self, new_blocks):
        """ mix the previous attributes blocks with new blocks by adding new ports to already declared blocks and new blocks with their ports to the list of blocks """
        pass


    def enrich_links(self, new_links):
        """ add new links if they haven't been already declared) """
        pass

    
    def convert_to_diag(self) -> DIAGFile:
        return(DIAGFile(self.name, self.blocks, self.links))