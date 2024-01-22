import os
import re

import numpy as np
import meshio

from fepy.node import Node
from fepy.element import E1L1,E1L2
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

def meshGen(input_file: str, order: int):
    """
    Generate the mesh with gmsh based on the type of element and order
    """
    # check that element order is below a certain treshold to prevent 
    if order > 3:
        raise ValueError("Element order is to high, select element order below 3")    


    # send shell command to generate mesh based on input order
    try:
        os.system("gmsh {0}.geo -order {1} -3".format(input_file,order))

        # if no error, return msh file
        return input_file + ".msh"

    except:
        raise SystemError("Error while generating mesh")

def inputReader(input_file):
     """
     Call the appropriate appropriate reader depending on the file format
     """
     # extract file format
     file_format = input_file.split(".")[-1]

     if file_format == "msh":
          return gmshParser(input_file)

     else:
         raise ValueError("Unssuported: '.{0}' file format. For now only '.gmsh' format is supported")


def gmshParser(input_file):
    """
    Parse gmsh file format input files to generate fe data
    """
    # read data in
    mesh = meshio.read(input_file)

    # initialize a node container
    nodes = []

    # Generate node data from meshio object
    """
    ****** Maybe consider not generating node data inside IO in case somehow one day, there may be particles 
    ****** instead of nodes
    """
    for node in mesh.points:
        nodes.append(Node(node[0], node[1], node[2]))

    # Retrieve element data
    vertex = []

    line = []
    line3 = []
    line4 = []

    triangle = []
    triangle6 = []
    triangle10 = []

    quad = []
    quad9 = []
    quad16 = []

    for cells in mesh.cells:

        # since arrays are inside arrays. Must use a list comprehension to extract all levels
        # of possible data in each type of cells
        match cells.type:
            case 'vertex':
                [vertex.append(arr) for arr in cells.data]

            case 'line':                 
                [line.append(arr) for arr in cells.data]

            case 'line3':
                [line3.append(arr) for arr in cells.data]

            case 'line4':
                [line4.append(arr) for arr in cells.data]

            case 'triangle':
                [triangle.append(arr) for arr in cells.data]

            case 'triangle6':
                [triangle6.append(arr) for arr in cells.data]

            case 'triangle10':
                [triangle10.append(arr) for arr in cells.data]

            case 'quad':
                [quad.append(arr) for arr in cells.data]

            case 'quad9':
                [quad9.append(arr) for arr in cells.data]

            case 'quad16':
                [quad16.append(arr) for arr in cells.data]
            
            case _:
                raise ValueError("cell type {0} invalid, check geo file for possible error leading to a error in .msh file". format(cells.type))


            # to do : 3d elements

    
    
    # Extract bcs data
    bcs_vertex = []

    bcs_line = []
    bcs_line3 = []
    bcs_line4 = []

    bcs_triangle = []
    bcs_triangle6 = []
    bcs_triangle10 = []

    bcs_quad = []
    bcs_quad9 = []
    bcs_quad16 = []

    for sets in mesh.cell_sets_dict:
        # loop over each sets and add to the correct bcs list
        pass
            


    

     


def main():
    pass
    

if __name__ == "__main__":
    main()