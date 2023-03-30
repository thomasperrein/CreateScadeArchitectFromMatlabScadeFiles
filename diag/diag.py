""" Definition of ARCHI File which is derived of XML file """

from model.block_port_link import Block, Link
from typing import List
from file.file import File


class DIAGFile(File):
    """ Diag file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        super().__init__(name, blocks, links)
        
        
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

