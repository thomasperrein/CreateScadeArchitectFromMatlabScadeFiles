#coding : utf-8
""" definition of the class Block """
from typing import List
from abc import ABC

PARAMETERS = ['name', 'color', 'label', 'textcolor',\
                'style','width','height', 'icon',\
                'background', 'shape']

class CSS(ABC):
    """ Classe CSS pour les cosmétiques des blocks """
    def __init__(self, name:str ='None', color:str =None, label:str = None, textcolor:str = None, \
        style: str = None, width: int = None, height: int = None, icon = None, background = None, \
        shape:str = None) -> None:
        """ Initialise une instance commune au port et au block pour toutes les cosmétiques """
        for param_name in PARAMETERS:
            param_value = locals()[param_name]
            setattr(self, param_name, param_value)

    
    def write_parameter(self, param:str, InARCHIFile= False):
        """ retourne le paramètre du block sous forme de string lisible par block diag """
        if InARCHIFile:
            if getattr(self,param) == None:
                return ""
            else:
                return f'{param} = "{getattr(self,param)}"'
        else:
            if getattr(self,param) == None:
                return ""
            else:
                if type(getattr(self,param)) == int or param == 'icon' or param == 'background':
                    return f'{param} = {getattr(self,param)}'
                else:
                    return f'{param} = "{getattr(self,param)}"'


    def write_attributes(self, InARCHIFile = False):
        """ methode pour implementer dans blockdiag le block avec attributs avec  """
        str_to_write = ''
        if InARCHIFile:
            for param in PARAMETERS[:]:
                if self.write_parameter(param, InARCHIFile) == "":
                    continue
                str_to_write += ' ' + self.write_parameter(param, InARCHIFile) 
            return str_to_write[1:]
        else:
            for param in PARAMETERS[1:]:
                if self.write_parameter(param, InARCHIFile) == "":
                    continue
                str_to_write += ' ' + self.write_parameter(param, InARCHIFile) + ','
            return f'[' + str_to_write[1:-1] + ']' #1:-1 to remove space blank and coma at the end
        


class Block(CSS):
    """ Block """
    def __init__(self, name: str = 'None', color: str = None, label: str = None, textcolor: str = None, style: str = None, width: int = None, height: int = None, icon=None, background=None, shape: str = None, usage:int = 0) -> None:
        super().__init__(name, color, label, textcolor, style, width, height, icon, background, shape)
        self.ports: List(Port) = []
        self.usage = usage
        
    
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


    def write_block_w_port(self,level_of_indentation='\t'):
        """ return the syntax to write block into the diagram """
        level_of_indentation_bis = level_of_indentation+level_of_indentation
        str_to_return = level_of_indentation + 'group ' + self.name + '_group' + ' {\n'
        for param in PARAMETERS[1:]:
            if param not in ['background','icon']:
                if self.write_parameter(param) == "":
                    continue
                str_to_return += level_of_indentation_bis + self.write_parameter(param) + ';\n'
        for port in self.get_all_ports():
            str_to_return += level_of_indentation_bis + port.name + ' ' + port.write_attributes() + ';\n'
        str_to_return += level_of_indentation_bis + self.name + ';\n'
        fake_block = Block()
        fake_port_I = InputPort(fake_block, self.name)
        fake_port_O = OutputPort(fake_block, self.name)
        for port in self.get_input_ports():
            temp_link = Link(port,fake_port_I,style='none')
            str_to_return += temp_link.write_link(level_of_indentation_bis) + ';\n'
        for port in self.get_output_ports():
            temp_link = Link(fake_port_O,port,style='none')
            str_to_return += temp_link.write_link(level_of_indentation_bis) + ';\n'
        str_to_return += level_of_indentation + '}\n'
        return str_to_return
    

    def add_usage(self):
        """ Add 1 to usage to know if the block is used or not """
        self.usage += 1 

    
""" Déclaration de la classe Port et de ses méthodes """

class Port(CSS,ABC):
    """ Classe abstraite pour désigner un port """
    def __init__(self, block: Block, name: str = None, color: str = None, label: str = None, textcolor: str = None, style: str = None, width: int = None, height: int = None, icon = None, background=None, numbered: int = None, shape: str = None) -> None:
        super().__init__(name, color, label, textcolor, style, width, height, icon, background, shape)
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

    def __init__(self, block: Block, name: str = 'None', color: str = None, label: str = None, textcolor: str = None, style: str = None, width: int = None, height: int = None, icon=None, background=None, numbered: int = None, shape: str = None) -> None:
        super().__init__(block, name, color, label, textcolor, style, width, height, icon, background, numbered, shape)


class OutputPort(Port):
    """ Classe spécifique d'output hérité de Port """

    port_type = 'output'

    def __init__(self, block: Block, name: str = 'None', color: str = None, label: str = None, textcolor: str = None, style: str = None, width: int = None, height: int = None, icon=None , background=None, numbered: int = None, shape: str = None) -> None:
        super().__init__(block, name, color, label, textcolor, style, width, height, icon, background, numbered, shape)


class InputOutputPort(InputPort, OutputPort):
    """ Classe spéicifique pour les in/out flow hérité de Port """
    pass


""" Déclaration classe de Lien entre les ports """

class Link(CSS):
    """ Lien """
    def __init__(self, output_port: OutputPort, input_port: InputPort, name: str = 'None', color: str = None, label: str = None, textcolor: str = None, style: str = None, width: int = None, height: int = None, icon=None, background=None, shape: str = None, dir=None) -> None:
        super().__init__(name, color, label, textcolor, style, width, height, icon, background, shape)
        self.input_port = input_port
        self.output_port = output_port
        self.dir = dir

    
    def change_input_port(self, input_port: InputPort):
        """ Changer le port input """
        self.input_port = input_port

    
    def change_output_port(self, output_port: OutputPort):
        """ Changer le port output"""
        self.output_port = output_port

    
    def write_link(self, level_of_indentation = '\t') -> str:
        """ retourne une chaine de caractère appropriée pour afficher le lien sous block diag"""
        if self.dir == None:
            return f'{level_of_indentation}{self.output_port.name} -> {self.input_port.name} ' + self.write_attributes()
        else:
            return f'{level_of_indentation}{self.output_port.name} -> {self.input_port.name} ' + self.write_attributes()[:-1] + ', ' + self.write_parameter('dir') + ']'
