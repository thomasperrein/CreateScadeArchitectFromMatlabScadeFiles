""" script to parse archi file and get object ARCHIFile at the end """
from archi.archi import ARCHIFile
from model.block_port_link import Block, InputPort, OutputPort, Link
import xml.etree.ElementTree as ET
import os
import archi.error_gestion as error

def parse_archi_file(path:str) -> ARCHIFile:
    """ parse an archi file in path (.archi extension required) and return an object with all properties of file """
    check = sanity_check(path)
    file_name = os.path.basename(path)
    file = os.path.splitext(file_name)[0]
    if not(check):
        raise error.SanityCheckError()
    else:
        tree = ET.parse(path)
        root = tree.getroot()
        blocks = []
        links = []
        ports = {}
        for child in root:
            if child.tag == "block":
                block = Block(**child.attrib)
                for port in list(child):
                    if port.tag == 'input':
                        instance = InputPort(block,**port.attrib)
                        ports[port.attrib['name']] = instance
                    elif port.tag == 'output':
                        instance = OutputPort(block,**port.attrib)
                        ports[port.attrib['name']] = instance
                    else:
                        raise error.PortError()
                blocks.append(block)
            elif child.tag == "link":
                for port in list(child):
                    if port.tag == 'input':
                        input_port = ports[port.attrib['name']]
                    elif port.tag == 'output':
                        output_port = ports[port.attrib['name']]
                    else:
                        raise error.PortError()
                link = Link(output_port=output_port, input_port=input_port, **child.attrib)
                links.append(link)
    return ARCHIFile(file,blocks,links)

def sanity_check(path:str) -> bool:
    """ Sanity check of the .archi file in input """
    file_ext = os.path.splitext(path)[1]
    return not(file_ext != '.archi' and file_ext != '.ARCHI')