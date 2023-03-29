""" Definition of ARCHI File which is derived of XML file """

from model.block_port_link import Block, Link, InputPort, OutputPort
from typing import List


class DIAGFile:
    """ Diag file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        """ method constructor to define object """
        self.name = name
        self.blocks = blocks
        self.links = links
        
        
    def write_diag_file(self, path:str) -> None:
        """ write the archi file corresponding to the object """
        f = open(path,'w')
        f.write('blockdiag admin {\n')
        for block in self.blocks:
            f.write(block.write_block_w_port())
        for link in self.links:
            f.write(link.write_link() + ';\n')
        f.write('}\n')
        print(f"File {self.name} written at {path}")

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



