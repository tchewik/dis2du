from .tree import RSTTree
from .convert2isanlp import convert2isanlp


def read_dis(filename):
    rst = RSTTree(filename)
    rst.build()
    return convert2isanlp(rst)
