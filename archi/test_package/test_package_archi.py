"""
Programme pour tester les fonctionnalités du Programme
"""
import sys
import filecmp
import os

sys.path.insert(0,r'../FindLinkBetweenNodesScade') # To be used if you want to test by running this program wo pytest

from model.block_port_link import Block, InputPort, OutputPort, Link

PATH = "archi/test_package/test.archi"
PATH2 = "archi/test_package/test2.archi"
PATH3 = "archi/test_package/test3.archi"

PATH_CLUSTER_IN = "archi/test_package/test_clustering_in.archi"
PATH_CLUSTER_TEST = "archi/test_package/test_clustering_test.archi"
PATH_CLUSTER_OUT = "archi/test_package/test_clustering_out.archi"

PATH_FAKE = "archi/test_package/test.fake"

import archi.parse_archi as archi
 
def test_writing_and_parsing():
    """ To test if the object are well written and parsed, check also if the function is symetric (s(s(path))=s(path))"""
    object = archi.parse_archi_file(PATH)
    object.write_archi_file(PATH2)
    object2 = archi.parse_archi_file(PATH2)
    object2.write_archi_file(PATH3)

    assert filecmp.cmp(PATH,PATH2)
    assert filecmp.cmp(PATH2,PATH3)

    os.remove(PATH2)
    os.remove(PATH3)

def test_clustering():
    object = archi.parse_archi_file(PATH_CLUSTER_IN)
    object.adapt_colors_w_clustering()
    object.write_archi_file(PATH_CLUSTER_TEST)
    assert filecmp.cmp(PATH_CLUSTER_OUT,PATH_CLUSTER_TEST)

    os.remove(PATH_CLUSTER_TEST)


def test_filecmp():
    """ Test de la comparaison de fichier et du caractère modificateur de adapt_colors_w_clustering """
    object = archi.parse_archi_file(PATH_CLUSTER_IN)
    diag_conv = object.convert_to_diag()
    assert diag_conv.filecmp(object)
    object.adapt_colors_w_clustering()
    assert diag_conv.filecmp(object)
    object.add_block(Block('new block'))
    assert not(diag_conv.filecmp(object))


def test_sanity_check():
    """ Test the sanity check """
    assert not(archi.sanity_check(PATH_FAKE))


def test_fusion_block():
    """ test fusion block """
    styleCSS_block = {
        'shape' : 'box'
    }
    styleCSS_port = {
            'color' : 'white',
            'icon' : "'static/input_output.png'",
            'shape' : 'box'
        }
    styleCSS_link = {
            'color' : 'black',
            'dir' : 'forward'
        }
    styleCSS_port2= {
            'color' : 'red',
            'icon' : "'static/input_output.png'",
            'shape' : 'box'
        }
    block1 = Block('block1',**styleCSS_block)
    block2 = Block('block2',**styleCSS_block)
    block3 = Block('block3',**styleCSS_block)
    block4 = Block('block4',**styleCSS_block)
    list_block = [block1, block2, block3, block4]
    archi_file = archi.ARCHIFile('test',[],[])
    archi_file.enrich_blocks(list_block)
    assert {block.name for block in archi_file.get_blocks()} == {block.name for block in list_block} #on teste si on retrouve les noms des blocks ajoutés dans l'archi file enrichi
    assert len(archi_file.get_blocks()) == len(list_block) #on teste si il n'y a pas des doublons qui se sont immiscés 
    assert archi_file.get_blocks()[0].shape == 'box' # test de la propagation de l'attribut 
    archi_file.enrich_blocks(list_block)
    assert {block.name for block in archi_file.get_blocks()} == {block.name for block in list_block} # test du caractère sos = s

    new_block1 = Block('new_block1',**styleCSS_block)
    new_block2 = Block('new_block2',**styleCSS_block)
    new_block3 = Block('new_block3',**styleCSS_block)
    new_block4 = Block('new_block4',**styleCSS_block)
    list_block = [new_block1, new_block2, new_block3, new_block4]
    archi_file.enrich_blocks(list_block)
    assert {block.name for block in archi_file.get_blocks()} == {'block1','block2','block3','block4','new_block1','new_block2','new_block3','new_block4'}
    assert not({block for block in archi_file.get_blocks()} == {block1, block2, block3, block4,new_block1, new_block2, new_block3, new_block4})
    new_block4.name = 'fake'
    assert {block.name for block in archi_file.get_blocks()} == {'block1','block2','block3','block4','new_block1','new_block2','new_block3','new_block4'}
    assert not({block for block in archi_file.get_blocks()} == {block1, block2, block3, block4,new_block1, new_block2, new_block3, new_block4})
    for block in list_block: #verification de l'enrichissement des ports pour les blocks déjà présents
        inport = InputPort(block, f'inport_{block.name}', **styleCSS_port)
        outport = OutputPort(block, f'outport_{block.name}', **styleCSS_port2)
    archi_file.enrich_blocks(list_block)
    assert {block.name for block in archi_file.get_blocks()} == {'block1','block2','block3','block4','new_block1','new_block2','new_block3','new_block4','fake'}
    corresp_block_name = {block.name : block for block in archi_file.get_blocks()}
    assert corresp_block_name['new_block1'].get_input_ports()[0].name == 'inport_' + corresp_block_name['new_block1'].name
    attrib = {key: value for key, value in corresp_block_name['new_block1'].get_input_ports()[0].__dict__.items() if not key.startswith("__")}
    assert attrib['color'] == 'white' # test de la propagation des attributs des ports
    assert attrib['icon'] == "'static/input_output.png'"
    assert attrib['shape'] == 'box'
    assert corresp_block_name['new_block1'].get_output_ports()[0].name == 'outport_' + corresp_block_name['new_block1'].name
    attrib = {key: value for key, value in corresp_block_name['new_block1'].get_output_ports()[0].__dict__.items() if not key.startswith("__")}
    assert attrib['color'] == 'red' # test de la propagation des attributs des ports
    assert attrib['icon'] == "'static/input_output.png'"
    assert attrib['shape'] == 'box'
    assert corresp_block_name['block1'].get_input_ports() == [] #pas d'enrichissiment des autres blocks
    assert corresp_block_name['block1'].get_output_ports() == []
    InputPort(block1,'a port', **styleCSS_port)
    assert corresp_block_name['block1'].get_input_ports() == []
    archi_file.enrich_blocks([block1])
    corresp_block_name = {block.name : block for block in archi_file.get_blocks()}
    assert corresp_block_name['block1'].get_input_ports()[0].name == 'a port'


def test_fusion_link():
    """ test fusion block """
    styleCSS_block = {
        'shape' : 'box'
    }
    styleCSS_port = {
            'color' : 'white',
            'icon' : "'static/input_output.png'",
            'shape' : 'box'
        }
    styleCSS_link = {
            'color' : 'black',
            'dir' : 'forward'
        }
    styleCSS_port2= {
            'color' : 'red',
            'icon' : "'static/input_output.png'",
            'shape' : 'box'
        }
    block1 = Block('block1',**styleCSS_block)
    block2 = Block('block2',**styleCSS_block)
    inport2 = InputPort(block2,'inport_block2',**styleCSS_port)
    outport1 = OutputPort(block1,'outport_block1',**styleCSS_port2)
    link = Link(outport1,inport2,**styleCSS_link)
    archi_file = archi.ARCHIFile('init',[block1,block2],[link])
    
    new_block = Block('block3')
    outport2 = OutputPort(block2,'outport_block2',**styleCSS_port2)
    inport3 = InputPort(new_block,'inport_block3', **styleCSS_port)
    link2 = Link(outport2,inport3,**styleCSS_link)
    link3 = Link(outport1,inport3,**styleCSS_link)
    new_links = [link2, link3]
    archi_file.enrich_blocks([new_block])
    archi_file.enrich_links(new_links)
    temp = []
    for lien in archi_file.get_links():
        temp.append(f'{lien.output_port.name} -> {lien.input_port.name}')
    assert {'outport_block1 -> inport_block2','outport_block2 -> inport_block3','outport_block1 -> inport_block3'} == set(temp)
    assert not({link,link2,link3} == {link in archi_file.get_links()})


if __name__ == '__main__':
    test_writing_and_parsing()
    test_clustering()
    test_filecmp()
    test_fusion_block()
    test_fusion_link()