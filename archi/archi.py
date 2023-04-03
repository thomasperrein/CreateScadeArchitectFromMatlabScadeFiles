""" Definition of ARCHI File which is derived of XML file """
from model.block_port_link import Block, Link, InputPort, OutputPort
from typing import List
from file.file import File
from diag.diag import DIAGFile
from api_matlab import data_from_subsystem_matlab
import copy
import sys
import os 

sys.path.append("C:\\Program Files\\ANSYS Inc\\v202\\SCADE\\SCADE\\APIs\\Python\\lib")
sys.path.append("C:\\Program Files\\ANSYS Inc\\v202\\SCADE\\SCADE\\bin")
sys.path.append("C:\\Program Files\\ANSYS Inc\\v202\\SCADE\\contrib\\Python37")
# sys.path.append("C:\\Users\\fx622208\\AppData\\Local\\Programs\\Python\\Python39\\DLLs")
os.environ["PATH"] = os.environ["PATH"] + "C:\\Program Files\\ANSYS Inc\\v202\\SCADE\\contrib\\Python37;"

import scade_env
import scade.model.suite, scade.model.project
import api_scade.scade_suite_file as sc
import re

class ARCHIFile(File):
    """ Archi file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        super().__init__(name, blocks, links)
        
        
    def write_archi_file(self, path:str) -> None:
        """ write the archi file corresponding to the object """
        f = open(path, 'w')
        f.write('<archi>\n')
        f.write(self.write_block())
        f.write(self.write_link())
        f.write('</archi>\n')
        f.close()
        print(f"File {self.name} written at {path}")


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


    def enrich_blocks(self, new_blocks: List[Block]):
        """ mix the previous attributes blocks with new blocks by adding new ports to already declared blocks and new blocks with their ports to the list of blocks """
        new_self_blocks = copy.deepcopy(self.blocks)
        correspondance_name_block = {block.name : block for block in new_self_blocks}
        for block in new_blocks: #For all the new blocks found
            if block.name in correspondance_name_block.keys(): #If it already exists => check if all the ports are the same
                name_port = [port.name for port in correspondance_name_block[block.name].get_all_ports()]
                for port in block.get_all_ports(): #So for all ports in the new block found
                    if not(port.name in name_port): #if it is not in the ports name already given
                        attrib = {key: value for key, value in port.__dict__.items() if not key.startswith("__")} # We add it by retrieve his attribute
                        attrib['block'] = correspondance_name_block[block.name] #change the block associated
                        if isinstance(port, InputPort):
                            InputPort(**attrib) #create a new inport with the same attribute except the block, which will be the one attached to the archi file
                        elif isinstance(port, OutputPort):
                            OutputPort(**attrib)
                        else:
                            continue
            else:
                new_self_blocks.append(copy.copy(block))
        self.blocks = new_self_blocks
        print('blocks added')


    def enrich_links(self, new_links: List[Link]):
        """ add new links if they haven't been already declared """
        new_self_links = copy.deepcopy(self.links)
        link_to_add = []
        for link_new in new_links:
            attrib = {key: value for key, value in link_new.__dict__.items() if not key.startswith("__")} # We add it by retrieve his attribute
            if len(new_self_links) == 0:
                link_to_add.append(Link(**attrib))
            else:
                for link_file in new_self_links:
                    if (link_new.input_port.name == link_file.input_port.name) & (link_new.output_port.name == link_file.output_port.name):
                        continue
                    else:
                        link_to_add.append(Link(**attrib))
                        break
        self.links = new_self_links + link_to_add
        print('links added')
    

    def enrich_link_block(self, new_blocks: List[Block], new_links: List[Link]):
        """ enrich with oth functions enrich link and enrich block """
        self.enrich_blocks(new_blocks)
        self.enrich_links(new_links)

    
    def enrich_archi_with_matlab(self, path_simulink:str, filepath:str, subsystems:list, path_api:str, CSS_block:dict, CSS_port:dict, CSS_link:dict):
        """ enrich archi file with matlab block into subsystems 
        Archi (and File by extension) is a MUTABLE object so wen you activate the function, it changes the object
        Returns : object changed
                "diag_object_after_matlab", its conversion in matlab (of the object enrich) 
                "before_object" the precedent object, without any changes 
        """
    
        list_of_blocks = []
        list_of_links = []

        correspondance_name_objet = {}

        data_matlab = data_from_subsystem_matlab.data_from_several_subsystem_matlab(path_simulink,filepath,subsystems,path_api)
        
        before_object = copy.deepcopy(self)

        for data in data_matlab:
            b = Block(data,**CSS_block)
            correspondance_name_objet[data] = b
            list_of_blocks.append(b)
            for e in data_matlab[data][0]['from']:
                if e['name'].split('/')[-1].replace('\n',"").replace(' ','_') not in correspondance_name_objet:
                    name_of_new_block = e['name'].split('/')[-1].replace('\n',"").replace(' ','_')
                    new_block = Block(name_of_new_block,**CSS_block)
                    list_of_blocks.append(new_block)
                    correspondance_name_objet[name_of_new_block] = new_block
                new_block = correspondance_name_objet[e['name'].split('/')[-1].replace('\n',"").replace(' ','_')]
                vv = OutputPort(new_block, e['port_associated'] + '_' + e['name'].split('/')[-1].replace('\n',"").replace(' ','_'), **CSS_port)
                v = InputPort(b, e['port_associated'] + '_' + data, **CSS_port)
                link = Link(vv,v,'link',**CSS_link)
                list_of_links.append(link)
            for e in data_matlab[data][0]['go']:
                if e['name'].split('/')[-1].replace('\n',"").replace(' ','_') not in correspondance_name_objet:
                    name_of_new_block = e['name'].split('/')[-1].replace('\n',"").replace(' ','_')
                    new_block = Block(name_of_new_block,**CSS_block)
                    list_of_blocks.append(new_block)
                    correspondance_name_objet[name_of_new_block] = new_block
                new_block = correspondance_name_objet[e['name'].split('/')[-1].replace('\n',"").replace(' ','_')]
                vv = InputPort(new_block, e['port_associated'] + '_' + e['name'].split('/')[-1].replace('\n',"").replace(' ','_'), **CSS_port)
                v = OutputPort(b, e['port_associated'] + '_' + data, **CSS_port)
                link = Link(v,vv,'link',**CSS_link)
                list_of_links.append(link)
        self.enrich_link_block(list_of_blocks, list_of_links)
        diag_object_after_matlab = self.convert_to_diag()
        return(self, diag_object_after_matlab, before_object)
    

    def enrich_archi_with_scade(self, PATH_SESSION_SCADE:str, styleCSS_block:dict, styleCSS_port:dict, styleCSS_link:dict):
        """ enrich archi file with matlab block into subsystems 
        Archi (and File by extension) is a MUTABLE object so wen you activate the function, it changes the object
        Returns : object changed
                "diag_object_after_matlab", its conversion in matlab (of the object enrich) 
                "before_object" the precedent object, without any changes 
        """
        list_of_inputs = []
        list_of_outputs = []
        list_of_blocks = []
        list_of_links = []

        scade_env.load_project(PATH_SESSION_SCADE)
        a = scade.model.suite.get_roots()[0]
        scade_object = sc.ScadeFileSuite(a)
        # data_scade = scade_object.data_of_interest()
        data_scade = scade_object.data_of_nodes()

        before_object = copy.deepcopy(self)

        for i in data_scade:
            b = Block(i,**styleCSS_block)
            for input in data_scade[i]['inputs']:
                v = InputPort(b,input + re.findall(r'_P\d+',i)[0],**styleCSS_port)
                list_of_inputs.append(v)
            for output in data_scade[i]['outputs']:
                vv = OutputPort(b,output + re.findall(r'_P\d+',i)[0],**styleCSS_port)
                list_of_outputs.append(vv)
            list_of_blocks.append(b)
        
        links = {}
        i = 0
        for b in list_of_blocks:
            ports_b = [re.sub(r'_P\d+$', "", port.name) for port in b.get_input_ports()]
            for bb in list_of_blocks:
                if b != bb:
                    ports_bb = [re.sub(r'_P\d+$', "", port.name) for port in bb.get_output_ports()]
                    set_common = set(ports_b) & set(ports_bb)
                    for e in set_common:
                        i += 1
                        links[f'link{i}']={'input': e + re.findall(r'_P\d+',b.name)[0],'output': e + re.findall(r'_P\d+',bb.name)[0]}
                        b.add_usage()
                        bb.add_usage()
        
        # def delete_unlinked_block(list_of_blocks: list = list_of_blocks,list_of_to_file: list = list_of_to_file):
        #     for b in list_of_blocks:
        #         if b.usage == 0:
        #             chaine = b.name
        #             for to_file in list_of_to_file:
        #                 temp = re.findall(chaine, to_file)
        #                 if len(temp) >= 1 :
        #                     list_of_to_file.remove(to_file)
                       
        fake_block = Block('a name')
        for link in links:
            list_of_links.append(Link(OutputPort(fake_block,links[link]['output']),InputPort(fake_block,links[link]['input']),link,**styleCSS_link))

        self.enrich_link_block(list_of_blocks,list_of_links)
        diag_object_after_scade = self.convert_to_diag()

        return(self, diag_object_after_scade, before_object)
        
            
    def convert_to_diag(self) -> DIAGFile:
        new_blocks = copy.copy(self.blocks)
        new_links = copy.copy(self.links)
        return(DIAGFile(self.name, new_blocks, new_links))