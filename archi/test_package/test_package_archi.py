"""
Programme pour tester les fonctionnalités du Programme
"""
import sys
import filecmp
import os

sys.path.insert(0,r'../FindLinkBetweenNodesScade') # To be used if you want to test by running this program wo pytest

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
    object = archi.parse_archi_file(PATH_CLUSTER_IN)
    diag_conv = object.convert_to_diag()
    assert diag_conv.filecmp(object)
    object.adapt_colors_w_clustering()
    assert diag_conv.filecmp(object)


def test_sanity_check():
    """ Test the sanity check """
    assert not(archi.sanity_check(PATH_FAKE))


if __name__ == '__main__':
    test_writing_and_parsing()
    test_clustering()