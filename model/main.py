#coding: utf-8
"""
Main programm to test firstly
"""

from block_port_link import Block, InputPort, OutputPort, Link


def main():
    """ main programm """
    block = Block(name='MyName',color='white')
    input_port_1 = InputPort(block,'Input1')
    input_port_2 = InputPort(block,'Input2')
    input_port_5 = InputPort(block, 'newinput')
    output_port_1 = OutputPort(block,'Output1')
    output_port_2 = OutputPort(block,'Output2')
    to_file = block.write_block_w_port()

    block2 = Block(name='Myname2',color='orange')
    input_port_3 = InputPort(block2,'Input3')
    input_port_4 = InputPort(block2,'Input4')
    output_port_3 = OutputPort(block2,'Output3')
    to_file2 = block2.write_block_w_port()

    link1 = Link(output_port_1,input_port_3)
    link2 = Link(output_port_2,input_port_4)

    f = open('my_file.diag','w')
    f.write('blockdiag admin {\n')
    f.write(to_file)
    f.write(to_file2)
    f.write(link1.write_link())
    f.write(link2.write_link())
    f.write('}\n')

if __name__ == "__main__":
    main()