"""
Programme pour tester les fonctionnalités du Programme
"""
import sys
import filecmp
import os

sys.path.insert(0, r'..\FindLinkBetweenNodesScade')

PATH = "archi/test_package/test.archi"
PATH2 = "archi/test_package/test2.archi"
PATH3 = "archi/test_package/test3.archi"

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


def test_sanity_check():
    """ Test the sanity check """
    assert not(archi.sanity_check(PATH_FAKE))


if __name__ == '__main__':
    test_writing_and_parsing()