#coding : utf-8
""" Déclaration classe de Lien entre les ports """
from model.block_port import *

class Link:
    """ Lien """
    def __init__(self, output_port: OutputPort, input_port: InputPort, dir='forward', label=None, style='solid') -> None:
        """ Initialisation """
        self.input_port = input_port
        self.output_port = output_port
        self.dir = dir
        self.label = label
        self.style = style

    
    def change_input_port(self, input_port: InputPort):
        """ Changer le port input """
        self.input_port = input_port

    
    def change_output_port(self, output_port: OutputPort):
        """ Changer le port output"""
        self.output_port = output_port

    
    def write_link(self) -> str:
        return f'\t{self.output_port.name} -> {self.input_port.name} [dir = {self.dir}, label = {self.label}, style =  {self.style}];\n'