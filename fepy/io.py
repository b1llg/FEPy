import os
import re

import numpy as np
import meshio

from fepy.node import Node
from fepy.element import E1LIN,E1QUD
from fepy.boundarycondition import EssentialBc, ImposedBc


class FemData:
    """
    Class that contains all the raw fem data
    """
    def __init__(self, elements: np.array, 
                 nodes: np.array, 
                 essential_bcs: np.array,
                 imposed_bcs: np.array):
        
        self.elements = elements
        self.nodes = nodes
        self.essential_bcs = essential_bcs
        self.imposed_bcs = imposed_bcs

def inputReader(input_file):
     """
     Call the appropriate appropriate reader depending on the file format
     """
     # extract file format
     file_format = input_file.split(".")[-1]

     if file_format == "msh":
          fem_data = gmshParser(input_file)
     else:
         raise ValueError("Unssuported: '.{0}' file format. For now only '.gmsh' format is supported")

def gmshParser(input_file):
     """
     Parse gmsh file format input files to generate fe data
     """
     mesh = meshio.read(input_file)

     nodes = []

    # Generate node data from meshio object
     for node in mesh.points:
         nodes.append(Node(node[0], node[1], node[2]))

    # 

     print(nodes)

     


def main():
    pass
    

if __name__ == "__main__":
    main()