from fepy.node import Node
import numpy as np
from abc import ABC

class BoundaryCondition(ABC):
    """
    Abstract class to instantiate boundary conditions
    """
    pass

class LoadBc(BoundaryCondition):
    """
    Boundary conditions applied to elements or node. These are conditions related to external values or natural conditions 
    Refers and entity id (eid or nid for element id or node id) by label. 
    Implementation is done in the main script
    """
    def __init__(self,label : str, dofs : list):
        self.label = label
        self.dofs = dofs

class EssentialBc(BoundaryCondition):
    """
    Boundary conditions applied to node. These are conditions related to the know value of the studied variable
    
    """
    def __init__(self, boundary_name : str, dofs : list):
        """
        Initialize an essential boundary conditions.

        boundary_name: must match the one created in the .geo file. The program will check later that 
            the boundary exists

        dofs: The length must match the number of dofs in the corresponding field 
            Will be checked later in the program. The value entered must corresponded
            to the value in the problem. For exemple [0,0] in a field where the displacement
            is analyzed, it means that the displacement is 0 on both degress of freedom for the
            selected boundary (boundary_name)
        """
        self.boundary_name = boundary_name
        self.dofs = dofs
