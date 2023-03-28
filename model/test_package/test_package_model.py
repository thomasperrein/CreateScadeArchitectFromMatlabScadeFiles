"""
Programme pour tester les fonctionnalités du Programme
"""
import sys
import filecmp
import os

sys.path.insert(0,r'../FindLinkBetweenNodesScade') # To be used if you want to test by running this program wo pytest

import model.block_port_link as block_port_link

PATH = "model/test_package/test.diag"
PATH_TEST = "model/test_package/test_test.diag"


def test_unit_block():
    block_test = block_port_link.Block('block1','white','label')
    assert block_test.name == 'block1'
    assert block_test.color == 'white'
    assert block_test.label == 'label'
    assert block_test.get_name() == 'block1'

    block_test.change_color('red')
    assert block_test.color == 'red'


    block_test.set_name('block11')
    assert block_test.name == 'block11'

    assert block_test.get_name() == 'block11'



def test_unit_port():
    block_port_test = block_port_link.Block('the block')

    port_test = block_port_link.InputPort(block_port_test,name='port1',color='red')
    assert port_test.name == 'port1'
    assert port_test.color == 'red'

    assert port_test.port_type == 'input'

    
    port_test_2 = block_port_link.OutputPort(block_port_test, name='port2')
    assert port_test_2.name == 'port2'
    assert port_test_2.color == None

    assert port_test_2.port_type == 'output'


def test_unit_link():
    blocked = block_port_link.Block()

    port1 = block_port_link.InputPort(blocked, 'Phy')
    port2 = block_port_link.OutputPort(blocked, 'Elec')

    link1 = block_port_link.Link(port2,port1)

    assert link1.output_port == port2
    assert link1.input_port == port1 

    new_port_1 = block_port_link.InputPort(blocked, 'Phy2')
    link1.change_input_port(new_port_1)

    assert link1.input_port == new_port_1

    new_port_2 = block_port_link.OutputPort(blocked, 'Elec2')
    link1.change_output_port(new_port_2)

    assert link1.output_port == new_port_2


def test_global():
    block1 = block_port_link.Block('block1')
    block2 = block_port_link.Block('aaaa')

    input_port_block2 = block_port_link.InputPort(block2,'Phy')

    assert input_port_block2.block == block2
    assert block2.ports == [input_port_block2]

    output_port_block1 = block_port_link.OutputPort(block1,'Elec')

    assert output_port_block1.block == block1
    assert block1.ports == [output_port_block1]

    output_port_block1.delete()
    assert block1.ports == []
    assert not(output_port_block1 in locals() or output_port_block1 in globals())

    output_port_block1_2 = block_port_link.OutputPort(block1,'Elec')
    
    assert output_port_block1_2.block == block1
    assert block1.ports == [output_port_block1_2] 

    link1 = block_port_link.Link(output_port_block1_2,input_port_block2)

    assert link1.write_link() == "\tElec -> Phy []"

def test_global_2():
    """ test global """
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
    to_file = block.write_block_w_port()

    block2 = block_port_link.Block(name='Myname2',color='orange')
    input_port_3 = block_port_link.InputPort(block2,'Input3', **styleCSS_port)
    input_port_4 = block_port_link.InputPort(block2,'Input4', **styleCSS_port)
    output_port_3 = block_port_link.OutputPort(block2,'Output3', **styleCSS_port)
    to_file2 = block2.write_block_w_port()

    link1 = block_port_link.Link(output_port_1,input_port_3,**styleCSS_link)
    link2 = block_port_link.Link(output_port_2,input_port_4,**styleCSS_link)

    f = open(PATH_TEST,'w')
    f.write('blockdiag admin {\n')
    f.write(to_file)
    f.write(to_file2)
    f.write(link1.write_link() + ';\n')
    f.write(link2.write_link() + ';\n')
    f.write('}\n')
    f.close()

    assert filecmp.cmp(PATH_TEST,PATH)

    os.remove(PATH_TEST)

