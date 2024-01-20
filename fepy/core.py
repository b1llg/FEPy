import os
from abc import ABC

import numpy as np

from fepy.io import inputReader

class FEtype(ABC):
    """
    defines type of finite element
    """
    pass

class Lagrangian(FEtype):
    """
    defines Lagrangians finite element type
    """
    pass

class Hermite(FEtype):
    """
    Defines Hermite finite element type
    """
    pass


class Space:
    """
    Defines the finite element space and calls the appropriate order in mesh generation
    """
    def __init__(self, fetype = Lagrangian, order = 1):
        """
        Initialize a finite element space for the model:
        input:  fetype: Type of finite element (LagrangianFE as default)
                order: order of the polynomials (1 as default)
        """
        self.fetype = fetype
        self.order = order


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
    A Model is what we are trying to solve
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

        self.fem_data = inputReader(input_file) 
        self.fields = field_array

        self.SetTotalDofs()
        pass

def main():
    pass

if __name__ == "__main__":
    main()