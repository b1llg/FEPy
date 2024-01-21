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
    def __init__(self, name : str, components: np.array):
        self.name = name
        self.components = components
        self.dof_per_node = components.size

class Model:
    """
    A Model is what we are trying to solve:
    input_file: name of the gmsh file (.geo extension) with full path
    field_array: array of all the fields to be solved
    space_array: array of all the space associated to each field
    """

    def SetTotalDofs(self):
        """
        Compute total dof to generate the stiffness matrix
        """
        
        # Initialize tdofs 
        self.tdofs = 0
        
        # Loop over fields and add the corresponding number of dofs
        # per node
        for field in self.fields:
            self.tdofs += field.dof_per_node * self.fem_data.nodes.size

    def __init__(self, input_file: str, field_array : np.array(Field), space_array : np.array(FEtype)):
        if field_array.size != space_array.size:
            raise ValueError("Field size is not the same size a space size")
        
        #Determine highest order
        order = 0
        for s in  space_array:
            # Loop over model spaces, determine equivalent order to generate adequate mesh
            if s.fetype.equiv_order(s.order) > order:
                order = s.fetype.equiv_order(s.order)

        # generate mesh
        mesh_file = meshGen(input_file, order)

        # read data from mesh file
        self.fem_data = inputReader(mesh_file) 

        self.fields = field_array

        self.SetTotalDofs()
        pass

def main():
    pass

if __name__ == "__main__":
    main()