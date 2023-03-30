"""
Programme pour tester les fonctionnalités du Programme
"""
import os
import sys
import filecmp
import model.block_port_link as block_port_link

sys.path.insert(0,r'../FindLinkBetweenNodesScade') # To be used if you want to test by running this program wo pytest

PATH = "diag/test_package/test.diag"
PATH_TRUE = "diag/test_package/test_true.diag"

import diag.diag as diag
 
def test_writing():
    """ To test if the object are well written """
    styleCSS_block = {
        'color' : 'white',
        'shape' : 'square'
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
    
    block = block_port_link.Block(name='MyName',**styleCSS_block)
    input_port_1 = block_port_link.InputPort(block,'Input1', **styleCSS_port)
    input_port_2 = block_port_link.InputPort(block,'Input2', **styleCSS_port)
    input_port_5 = block_port_link.InputPort(block, 'newinput', **styleCSS_port)
    output_port_1 = block_port_link.OutputPort(block,'Output1', **styleCSS_port)
    output_port_2 = block_port_link.OutputPort(block,'Output2', **styleCSS_port)

    block2 = block_port_link.Block(name='Myname2',color='orange')
    input_port_3 = block_port_link.InputPort(block2,'Input3', **styleCSS_port)
    input_port_4 = block_port_link.InputPort(block2,'Input4', **styleCSS_port)
    output_port_3 = block_port_link.OutputPort(block2,'Output3', **styleCSS_port)

    link1 = block_port_link.Link(output_port_1,input_port_3,**styleCSS_link)
    link2 = block_port_link.Link(output_port_2,input_port_4,**styleCSS_link)

    blocks = [block, block2]
    links = [link1, link2]

    object_diagfile = diag.DIAGFile('name', blocks, links)
    object_diagfile.write_diag_file(PATH)

    assert filecmp.cmp(PATH, PATH_TRUE)
    assert object_diagfile.name == 'name'
    assert object_diagfile.links == links
    assert object_diagfile.blocks == blocks

    os.remove(PATH)

def test_file_cmp():
    styleCSS_block = {
        'color' : 'white',
        'shape' : 'square'
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
    
    block = block_port_link.Block(name='MyName',**styleCSS_block)
    input_port_1 = block_port_link.InputPort(block,'Input1', **styleCSS_port)
    input_port_2 = block_port_link.InputPort(block,'Input2', **styleCSS_port)
    input_port_5 = block_port_link.InputPort(block, 'newinput', **styleCSS_port)
    output_port_1 = block_port_link.OutputPort(block,'Output1', **styleCSS_port)
    output_port_2 = block_port_link.OutputPort(block,'Output2', **styleCSS_port)

    block2 = block_port_link.Block(name='Myname2',color='orange')
    input_port_3 = block_port_link.InputPort(block2,'Input3', **styleCSS_port)
    input_port_4 = block_port_link.InputPort(block2,'Input4', **styleCSS_port)
    output_port_3 = block_port_link.OutputPort(block2,'Output3', **styleCSS_port)

    link1 = block_port_link.Link(output_port_1,input_port_3,**styleCSS_link)
    link2 = block_port_link.Link(output_port_2,input_port_4,**styleCSS_link)

    blocks = [block, block2]
    links = [link1, link2]

    object_diagfile = diag.DIAGFile('name', blocks, links)
    
    assert object_diagfile.filecmp(object_diagfile)
    
if __name__ == '__main__':
    test_writing()