""" Scade OSD Architect object"""
from file import file 
from typing import List
from abc import ABC
from model.block_port_link import Block, Link

PARAMETERS = ['Kind', 'Name', 'Priority', 'Offset', \
                'Period', 'Deadline', 'SwExecutionUnit',\
                    'PValue', 'Immediate', 'Source', \
                'Target', 'Direction','Type'
]

class ScadeArchitectOSDObject(ABC):
    """ Object that contains all info of and OSD architect file """
    def __init__(self, Kind:str = None, Name:str = None, Priority:str = None, Offset:str = None, Period:str = None, Deadline:str = None, SwExecutionUnit:str = None, PValue:str = None, Immediate:str = None, Source:str = None, Target:str = None, Direction:str = None, Type:str = None) -> None:
        for param_name in PARAMETERS:
            param_value = locals()[param_name]
            setattr(self, param_name, param_value)
    

    def write_object_csv(self):
        output = ''
        for param in PARAMETERS:
            if getattr(self,param) == None:
                output += ';'
            else:
                output += getattr(self,param) + ';'
        return output[:-1]
    

class ScadeArchitectOSDInput(ScadeArchitectOSDObject):
    """ Object """
    def __init__(self, Kind: str = None, Name: str = None, Priority: str = None, Offset: str = None, Period: str = None, Deadline: str = None, SwExecutionUnit: str = None, PValue: str = None, Immediate: str = None, Source: str = None, Target: str = None, Direction: str = None, Type: str = None) -> None:
        super().__init__('System::AtomicFlowPort', Name, None, None, None, None, None, None, None, None, None, 'in', Type)


class ScadeArchitectOSDOutput(ScadeArchitectOSDObject):
    """ Object """
    def __init__(self, Kind: str = None, Name: str = None, Priority: str = None, Offset: str = None, Period: str = None, Deadline: str = None, SwExecutionUnit: str = None, PValue: str = None, Immediate: str = None, Source: str = None, Target: str = None, Direction: str = None, Type: str = None) -> None:
        super().__init__('System::AtomicFlowPort', Name, None, None, None, None, None, None, None, None, None, 'out', Type)


class ScadeArchitectOSDBlock(ScadeArchitectOSDObject):
    """ Object """
    def __init__(self, Kind: str = None, Name: str = None, Priority: str = None, Offset: str = None, Period: str = None, Deadline: str = None, SwExecutionUnit: str = None, PValue: str = None, Immediate: str = None, Source: str = None, Target: str = None, Direction: str = None, Type: str = None) -> None:
        super().__init__('OpenSystemDescription::Function', Name, Priority, Offset, Period, Deadline, SwExecutionUnit, None, None, None, None, None, None)


class ScadeArchitectOSDSystem(ScadeArchitectOSDObject):
    """ Object """
    def __init__(self, Kind: str = None, Name: str = None, Priority: str = None, Offset: str = None, Period: str = None, Deadline: str = None, SwExecutionUnit: str = None, PValue: str = None, Immediate: str = None, Source: str = None, Target: str = None, Direction: str = None, Type: str = None) -> None:
        super().__init__('OpenSystemDescription::System', 'System', None, None, None, None, None, None, None, None, None, None, None)


class ScadeArchitectOSDCommunications(ScadeArchitectOSDObject):
    """ Object """
    def __init__(self, Kind: str = None, Name: str = None, Priority: str = None, Offset: str = None, Period: str = None, Deadline: str = None, SwExecutionUnit: str = None, PValue: str = None, Immediate: str = None, Source: str = None, Target: str = None, Direction: str = None, Type: str = None) -> None:
        super().__init__('OpenSystemDescription::Communication', Name, None, None, None, None, None, PValue, Immediate, Source, Target, None, None)


class ScadeArchitectOSDCSV(file.File):
    """ Object """
    def __init__(self, name: str, blocks: List[Block], links: List[Link]) -> None:
        super().__init__(name, blocks, links)

    def write_header(self, parameters = PARAMETERS):
        output1 = ';;'
        output2 = ';;'
        for count,param in enumerate(PARAMETERS):
            ascii_code = chr(((count) % 26) + 65)
            if param == 'Kind':
                output2 += '(Kind);'
                output1 += ascii_code + ';'
            else:
                output2 += param + ';'
                output1 += ascii_code + ';'
        return output1[:-1] + '\n' + output2[:-1] + '\n'


    def write_csv(self, path):
        f = open(path, 'w', encoding='utf-8')
        f.write(self.write_header())
        index = 0
        number_coma = len(PARAMETERS) - 1
        f.write(f'{index};Blocks;' + number_coma*';' + '\n')
        index += 1
        f.write(f'{index};  System;' + ScadeArchitectOSDSystem().write_object_csv() + '\n')
        index += 1
        f.write(f'{index};    Replicas;' + number_coma*';' + '\n')
        index += 1
        for block in self.blocks:
            name_of_block = block.name
            temp_obj_block = ScadeArchitectOSDBlock(Name = name_of_block)
            f.write(f'{index};      {name_of_block};' + temp_obj_block.write_object_csv() + '\n')
            index += 1
            f.write(f'{index};        Ports;' + number_coma*';' + '\n')
            index += 1
            for port in block.get_input_ports():
                name_of_port = port.name
                temp_obj_port = ScadeArchitectOSDInput(Name = name_of_port)
                f.write(f'{index};          {name_of_port};' + temp_obj_port.write_object_csv() + '\n')
                index += 1
            for port in block.get_output_ports():
                name_of_port = port.name
                temp_obj_port = ScadeArchitectOSDOutput(Name = name_of_port)
                f.write(f'{index};          {name_of_port};' + temp_obj_port.write_object_csv() + '\n')
                index += 1
        f.write(f'{index};    Communications;' + number_coma*';' + '\n')
        index += 1
        for count,link in enumerate(self.links):
            input_port_name = link.input_port.name
            input_block_name = link.input_port.block.name
            output_port_name = link.output_port.name
            output_block_name = link.output_port.block.name
            link_name = output_block_name + '_Data' +  str(count+1)
            temp_obj_link = ScadeArchitectOSDCommunications(Name = link_name, PValue='0', Immediate='false', Source=output_block_name+'.'+output_port_name, Target=input_block_name+'.'+input_port_name)
            f.write(f'{index};      {link_name};' + temp_obj_link.write_object_csv() + '\n')
            index += 1
        f.close()
