"""
Test file
"""
import sys 

sys.path.insert(0,r'../FindLinkBetweenNodesScade')
from file.file import File
from model.block_port_link import Block, Link, InputPort, OutputPort

def test_add_block():
    """ test unitaire add block """
    blocks = [Block("1"), Block("2")]
    file = File("file", blocks, [])
    block = Block("3")
    file.add_block(block)
    assert block in file.get_blocks()

def test_add_link():
    """ test unitaire add link """
    fake_block = Block()
    port1 = InputPort(fake_block, 'Phy')
    port2 = OutputPort(fake_block, 'Elec')
    port3 = OutputPort(fake_block, 'Mat')
    port4 = InputPort(fake_block, 'Bio')
    links = [Link(port2, port1), Link(port3, port1)]
    file = File("file", [], links)
    link = Link(port3, port4)
    file.add_link(link)
    assert link in file.get_links()

def test_get_blocks():
    """ test unitaire get block """
    blocks = [Block("1"), Block("2")]
    file = File("file", blocks, [])
    assert file.get_blocks() == blocks

def test_get_links():
    """ test unitaire get link """
    fake_block = Block()
    port1 = InputPort(fake_block, 'Phy')
    port2 = OutputPort(fake_block, 'Elec')
    port3 = OutputPort(fake_block, 'Mat')
    links = [Link(port2, port1), Link(port3, port1)]
    file = File("file", [], links)
    assert file.get_links() == links

def test_filecmp():
    """ test unitaire filecmp """
    blocks = [Block("1"), Block("2")]
    fake_block = Block()
    port1 = InputPort(fake_block, 'Phy')
    port2 = OutputPort(fake_block, 'Elec')
    port3 = OutputPort(fake_block, 'Mat')
    links = [Link(port2, port1), Link(port3, port1)]
    file1 = File("file1", blocks, links)
    file2 = File("file2", blocks, links)
    assert file1.filecmp(file2) is True
