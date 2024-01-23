import os

import numpy as np

from fepy.io import inputReader, meshGen
from fepy.space import FEtype, Lagrangian, Hermite, MINI


class Field:
    """
    A field is what is studied. 
    - Heat Transfer : Temperature (scalar)
    - Solid Mechanics: Displacement (vector)
    """
    def __init__(self, name : str, components: list):
        self.name = name
        self.components = components
        self.dof_per_node = len(components)

class Model:
    """
    A Model is what we are trying to solve:
    input_file: name of the gmsh file (.geo extension) with full path
    field_array: array of all the fields to be solved
    space_array: array of all the space associated to each field
    """

    def __init__(self, input_file: 
                 str, field_array : list, 
                 space_array : list):
        
        if len(field_array) != len(space_array):
            raise ValueError("Field size is not the same size a space size")
        
        #Determine highest order
        order = 0
        for s in  space_array:
            # Loop over model spaces, determine equivalent order to generate adequate mesh
            if s.fetype.equiv_order(s.order) > order:
                order = s.fetype.equiv_order(s.order)

        # generate mesh
        mesh_file = meshGen(input_file, order)

        # get raw data from input file
        self.fem_data = inputReader(mesh_file) 

        #Parse raw data and associate gmsh data to FEpy element formulation
        self.fields = field_array


def main():
    pass

if __name__ == "__main__":
    main()