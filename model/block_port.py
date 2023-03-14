#coding : utf-8
""" definition of the class Block """
from typing import List
from abc import ABC

PARAMETERS = ['name', 'color', 'label', 'textcolor',\
                'style','width','height', 'icon',\
                'background', 'shape']

class CSS(ABC):
    """ Classe CSS pour les cosmétiques des blocks """
    def __init__(self, name:str ='None', color:str ='white', label:str = None, textcolor:str = 'black', \
        style: str = 'dotted', width: int = 100, height: int = 50, icon = None, background = None, \
        shape:str = 'rectangle') -> None:
        """ Initialise une instance commune au port et au block pour toutes les cosmétiques """
        for param_name in PARAMETERS:
            param_value = locals()[param_name]
            setattr(self, param_name, param_value)
    
    def write(self):
        """ methode pour implementer dans blockdiag le port """
        str_to_write = ''
        for param in PARAMETERS[1:]:
            str_to_write += f' {param} = {getattr(self,param)},'
        return f'{self.name} [' + str_to_write[1:-1] + '];\n'
        
class Block(CSS):
    """ Block """
    def __init__(self, name: str = 'None', color: str = 'white', label: str = None, textcolor: str = 'black', style: str = 'dotted', width: int = 100, height: int = 50, icon="'static/vide.png'", background="'static/logo.png'", numbered: int = None, shape: str = 'rectangle') -> None:
        super().__init__(name, color, label, textcolor, style, 100, 50, icon, background, 'box')
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
            str_to_return += level_of_indentation_bis + port.write()
        str_to_return += level_of_indentation_bis + self.name + ';\n'
        for port in self.get_input_ports():
            str_to_return += level_of_indentation_bis + f'{port.name} -> {self.name} [style = none];\n'
        for port in self.get_output_ports():
            str_to_return += level_of_indentation_bis + f'{self.name} -> {port.name} [style = none];\n'
        str_to_return += level_of_indentation + '}\n'
        return str_to_return
    
""" Déclaration de la classe Port et de ses méthodes """

class Port(CSS,ABC):
    """ Classe abstraite pour désigner un port """
    def __init__(self, block: Block, name: str = 'None', color: str = 'white', label: str = None, textcolor: str = 'black', style: str = 'dotted', width: int = 100, height: int = 50, icon="'static/vide.png'", background="'static/input_output.png'", numbered: int = None, shape: str = 'rectangle') -> None:
        super().__init__(name, color, label, textcolor, style, 25, 25, icon, background, shape='circle')
        self.block = block
        block.ports.append(self)


    def get_name(self):
        """ méthode pour récuperer le nom du Port """
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



class InputPort(Port):
    """ Classe spécifique d'input hérité de Port """

    port_type = 'input'

    def __init__(self, block: Block, name: str = 'None', color: str = 'white', label: str = None, textcolor: str = 'black', style: str = 'dotted', width: int = 25, height: int = 25, icon="'static/vide.png'", background="'static/input_output.png'", shape: str = 'rectangle') -> None:
        super().__init__(block, name, color, label, textcolor, style, width, height, icon, background, shape)


class OutputPort(Port):
    """ Classe spécifique d'output hérité de Port """

    port_type = 'output'

    def __init__(self, block: Block, name: str = 'None', color: str = 'white', label: str = None, textcolor: str = 'black', style: str = 'dotted', width: int = 25, height: int = 25, icon="'static/vide.png'", background="'static/input_output.png'", shape: str = 'rectangle') -> None:
        super().__init__(block, name, color, label, textcolor, style, width, height, icon, background, shape)


class InputOutputPort(InputPort, OutputPort):
    """ Classe spéicifique pour les in/out flow hérité de Port """
    pass