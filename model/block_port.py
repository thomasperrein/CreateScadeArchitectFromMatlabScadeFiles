#coding : utf-8
""" definition of the class Block """
from typing import List
from abc import ABC

class Block:
    """ Block """
    def __init__(self, name='None', color='white', label='None'):
        """ Initialise les attributs d'instance """
        self.name = name
        self.color = color
        self.label = label
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


    def write_label(self):
        """ retourne le label du block sous forme de string lisible par block diag """
        return f'label = "{self.label}";\n'


    def write_color(self):
        """ retourne le label du block sous forme de string lisible par block diag """
        return f'color = "{self.color}";\n'


    def write_block_w_port(self,level_of_indentation='\t'):
        """ return the syntax to write block into the diagram """
        level_of_indentation_bis = level_of_indentation+level_of_indentation
        str_to_return = level_of_indentation + 'group ' + self.name + '_group' + ' {\n'
        str_to_return += level_of_indentation_bis + self.write_label()
        str_to_return += level_of_indentation_bis + self.write_color()
        for port in self.get_all_ports():
            str_to_return += level_of_indentation_bis + port.write_port()
        str_to_return += level_of_indentation_bis + self.name + ';\n'
        for port in self.get_input_ports():
            str_to_return += level_of_indentation_bis + f'{port.name} -> {self.name} [dir = none, style = dashed];\n'
        for port in self.get_output_ports():
            str_to_return += level_of_indentation_bis + f'{self.name} -> {port.name} [dir = none, style = dashed];\n'
        str_to_return += level_of_indentation + '}\n'
        return str_to_return
    
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

    
    def delete(self):
        self.block.ports.remove(self)
        del self

    
    def write_port(self):
        """ methode pour implementer dans blockdiag le port """
        return f'{self.name} [shape = circle];\n'



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