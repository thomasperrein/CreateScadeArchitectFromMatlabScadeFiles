"""
Programme pour tester les fonctionnalités du Programme
"""

import model.block_port_link as block_port_link
 
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
    assert port_test_2.color == 'white'

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

    assert link1.write_link() == "\tElec -> Phy [dir = forward, label = None, style = None];\n"
