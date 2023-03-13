#coding : utf-8
""" definition of the class Block """
from typing import List
from abc import ABC

class Block:
    """ Block """
    def __init__(self, name='None', color='white'):
        """ Initialise les attributs d'instance """
        self.name = name
        self.color = color
        self.ports: List(Port) = []
    
    def set_name(self, name):
        """ methode pour set le nom du block """
        self.name = name

    
    def get_name(self):
        """ methode pour avoir le nom du block """
        return(self.name)


    def change_color(self,color):
        """ méthode pour changer la couleur d'affichage du block """
        self.color = color
    

    def write_block(self) -> str:
        """ Ecriture du bloc dans block diagram """
        return f'[label = "{self.name}"]'


    def get_input_ports(self) -> list:
        """ Recupère la liste des ports de type input associés au block """
        input_ports = []
        for port in self.ports:
            if isinstance(port, InputPort):
                input_ports.append(port)
        return input_ports
    

    def get_output_ports(self) -> list:
        """ Recupère la liste des ports de type output associés au block """
        output_ports = []
        for port in self.ports:
            if isinstance(port, OutputPort):
                output_ports.append(port)
        return output_ports
    

    def get_all_ports(self) -> list:
        """ Retourne la liste de tous les ports associés au block """
        return self.ports
    
""" Déclaration de la classe Port et de ses méthodes """

class Port(ABC):
    """ Classe abstraite pour désigner un port """
    def __init__(self, block: Block, name='None', color='color') -> None:
        """ Initialise la classe Port et ses attributs """
        self.name = name
        self.color = color
        self.block = block
        block.ports.append(self)


    def get_name(self):
        """ méthoe pour récuperer le nom du Port """
        return self.name

    
    def set_name(self, name):
        """ méthode pour set le nom de Port """
        self.name = name


    def get_block(self):
        """ methode pour avoir le block lié au port depuis l'objet port"""
        return self.block

    
    def __del__(self):
        print(f"object {self.name} deleted")
        print([port.name for port in self.block.ports])
        self.block.ports.remove(self)



class InputPort(Port):
    """ Classe spécifique d'input hérité de Port """

    port_type = 'input'

    def __init__(self, block: Block, name='None', color='color') -> None:
        super().__init__(block, name, color)


class OutputPort(Port):
    """ Classe spécifique d'output hérité de Port """
    port_type = 'output'

    def __init__(self, block: Block, name='None', color='color') -> None:
        super().__init__(block, name, color)


class InputOutputPort(InputPort, OutputPort):
    """ Classe spéicifique pour les in/out flow hérité de Port """
    pass