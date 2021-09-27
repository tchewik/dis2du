## tree.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 10/01/2014 15:01:09>

""" Any operation about an RST tree should be here
1, Build general/binary RST tree from annotated file
2, Binarize a general RST tree to the binary form
3, Generate bracketing sequence for evaluation
4, Write an RST tree into file (not implemented yet)
5, Generate Shift-reduce parsing action examples
6, Get all EDUs from the RST tree
- YJ
"""

from .buildtree import *


class RSTTree(object):
    def __init__(self, fname=None, tree=None):
        """ Initialization

        :type text: string
        :param text: dis file content
        """
        self.fname = fname
        self.binary = True
        self.tree = tree

    def build(self):
        """ Build BINARY RST tree
        """
        text = open(self.fname).read()
        self.tree = buildtree(text)
        self.tree = binarizetree(self.tree)
        self.tree = backprop(self.tree)
