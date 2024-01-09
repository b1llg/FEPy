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
        self.tdofs = 0
        
        for field in self.fields:
            self.tdofs += field.dof_per_node * self.fem_data.nodes.size

    def __init__(self, fem_data : FemData, field_array : np.array(Field) ):
        self.fem_data = fem_data
        self.fields = field_array

        self.SetTotalDofs()
        pass

def main():
    pass

if __name__ == "__main__":
    main()