import numpy as np

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
