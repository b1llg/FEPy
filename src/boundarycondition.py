from node import Node
import numpy as np
from abc import ABC

class BoundaryCondition(ABC):
    """
    Abstract class to instantiate boundary conditions
    """
    pass

class ImposedBc(BoundaryCondition):
    """
    Boundary conditions applied to elements or node. These are conditions related to external values or natural conditions 
    Refers and entity id (eid or nid for element id or node id) by label. 
    Implementation is done in the main script
    """
    def __init__(self,label : str, entity_ids : np.array):
        self.label = label
        self.entity_ids = entity_ids

class EssentialBc(BoundaryCondition):
    """
    Boundary conditions applied to node. These are conditions related to the know value of the studied variable
    
    """
    def __init__(self, nodes: np.array, dofs: np.ndarray):
        self.nodes = nodes
        self.dofs = dofs
