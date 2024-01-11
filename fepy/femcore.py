import numpy as np
from ioutils import inputReader


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

    def __init__(self, input_file: str, field_array : np.array(Field) ):
        self.fem_data = inputReader(input_file) 
        self.fields = field_array

        self.SetTotalDofs()
        pass

def main():
    pass

if __name__ == "__main__":
    main()