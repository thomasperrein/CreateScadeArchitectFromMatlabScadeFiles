""" 
Classe qui définit des propriétés et des méthodes communes à tous les objets fichiers 
"""
import numpy as np
from model.block_port_link import Block, Link
from typing import List
from abc import ABC
from numpy import array, linspace
from sklearn.neighbors import KernelDensity
from scipy.signal import argrelextrema

class File(ABC):
    """ classe File pour hériter de fonctions communes à diag, archi"""
    COLOR_CLUSTERS = ["green","blue","orange","red"]

    def __init__(self, name:str, blocks:List[Block], links:List[Link]) -> None:
        """ method constructor to define object """
        self.name = name
        self.blocks = blocks
        self.links = links


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

        
    def filecmp(self, other_file) -> bool:
        """ compare two files """
        set_self_blocks = set(self.blocks)
        set_self_links = set(self.links)
        set_cmp_blocks = set(other_file.blocks)
        set_cmp_links = set(other_file.links)
        return(set_cmp_blocks == set_self_blocks) & (set_cmp_links == set_self_links)

    
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


        def write_csv(path:str):
            f = open(path, 'w', encoding='utf-8')
            f.close()