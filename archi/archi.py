""" Definition of ARCHI File which is derived of XML file """

from model.block_port_link import Block, Link, InputPort, OutputPort
from typing import List


class ARCHIFile:
    """ Archi file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        """ method constructor to define object """
        self.name = name
        self.blocks = blocks
        self.links = links
        
        
    def write_archi_file(self, path:str) -> None:
        """ write the archi file corresponding to the object """
        
        f = open(path, 'w')
        f.write('<archi>\n')
        f.write(self.write_block())
        f.write(self.write_link())
        f.write('</archi>\n')
        f.close()
        print(f"File {self.name} written in {path}")

    def add_block(self, block:Block):
        """ add a block to the class """
        self.blocks.append(block)

    def add_link(self, link:Link):
        """ add a link to the class """
        self.links.append(link)

    def get_blocks(self):
        """ return the blocks of the class """
        return self.blocks

    def get_links(self):
        """ return the links of the class """
        return self.links

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


