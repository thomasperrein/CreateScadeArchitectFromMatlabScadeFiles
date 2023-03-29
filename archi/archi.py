""" Definition of ARCHI File which is derived of XML file """
import numpy as np
from model.block_port_link import Block, Link
from typing import List
from numpy import array, linspace
from sklearn.neighbors import KernelDensity
from scipy.signal import argrelextrema

class ARCHIFile:

    COLOR_CLUSTERS = ["green","blue","orange","red"]
    """ Archi file object """
    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        """ method constructor to define object """
        self.name = name
        self.blocks = blocks
        self.links = links
        
        
    def write_archi_file(self, path:str) -> None:
        """ write the archi file corresponding to the object """
        f = open(path, 'w')
        f.write('<archi>\n')
        f.write(self.write_block())
        f.write(self.write_link())
        f.write('</archi>\n')
        f.close()
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


    def enrich_blocks(self, new_blocks):
        """ mix the previous attributes blocks with new blocks by adding new ports to already declared blocks and new blocks with their ports to the list of blocks """
        pass


    def enrich_links(self, new_links):
        """ add new links if they haven't been already declared) """
        pass


    def adapt_colors_w_clustering(self, k:int = 10):
        """ allow to change color of blocks in the file according to the number of ports they have
        Works only if there are more than two blocks in the file ! 
        k : integer to adjust sensitivity, default value 10 """ 
        if len(self.blocks) <= 4:
            con_block_nb_ports = {}
            list_of_values = []
            for block in self.blocks:
                con_block_nb_ports[len(block.get_all_ports())] = block
                list_of_values.append(len(block.get_all_ports()))
            new_list = sorted(list_of_values)
            for i in range(len(new_list)):
                value = new_list[i]
                con_block_nb_ports[value].change_color(self.COLOR_CLUSTERS[i])
        else:  
            a = array([len(block.get_all_ports()) for block in self.blocks]).reshape(-1,1)
            kde = KernelDensity(kernel='gaussian', bandwidth=3).fit(a)
            s = linspace(0,max(a)+k)
            e = kde.score_samples(s.reshape(-1,1))

            mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
            
            clusters = []
            for i in range(len(mi)):
                if i==0:
                    clusters.append(a[a < s[mi][0]])
                elif i==(len(mi)-1):
                    clusters.append(a[a >= s[mi][-1]])
                else:
                    clusters.append(a[(a >= s[mi][i]) * (a <= s[mi][i+1])])
            clustered_block = {'0':[],
                                '1':[],
                                '2':[],
                                '3':[]}
            for block in self.blocks:
                nb_ports = len(block.get_all_ports())
                for i in range(len(clusters)):
                    if nb_ports in clusters[i]:
                        clustered_block[f'{i%4}'].append(block)
            for i in range(4):
                blocks = clustered_block[f'{i}']
                for block in blocks:
                    block.change_color(self.COLOR_CLUSTERS[i])