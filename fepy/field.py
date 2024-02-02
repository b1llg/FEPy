import os

import numpy as np

import fepy.domain

class Field:
    """
    A FEM function is either a trial or test function 
    """
    def add_domain(self,domain: fepy.domain.Domain):
        self.domains[domain] = fepy.domain.Domain()

    def add_boundary(self, boundary : str):
        self.boundaries[boundary] = fepy.domain.Boundary()

    def set_domain(self, fem_data: fepy.io.FemData, space: fepy.space.Space):
        """
        Add domain definition. Loop over fem_data and check domains defined in file and add them to their respective field
        """
        for domain in self.domains:
            for fd_domain in fem_data.domains:
                if fd_domain == domain:
                    for eltype, elements in fem_data.domains[fd_domain].items():
                        # retrieve node definition for all elements
                        for el in elements:
                            nodes = fem_data.elements[el]
                            self.domains[domain].append(set_element(eltype, nodes, space))

    def set_boundaries(self, fem_data: fepy.io.FemData, space: fepy.space.Space):
        """
        Add boundary definition. Loop over fem_data and check boundaries defined in file and add them
        to their respective boundary in field obejct
        """
        for domain in fem_data.domains:
            pass

    def set_element(element_type : str, nodes : np.ndarray, space: fepy.space.Space):
        """
        Convert the basic raw data to the correct element formulation
        depending on the function space provied

        fem_data: raw fem_data extracted from the generated mesh file

        sapce: function space associated to the current field behind builded
        """
        # for each element of the current type, use class_init which calls the
        # good initializer for the current type -> fepy.element
        # special case for vertex 

        parsed_element = []

        if element_type == 'vertex':
            parsed_element.append(fepy.node.Node(nodes[0],
                                                     nodes[1],
                                                     nodes[2]))
        else:
            # get the type of space function
            class_init = fepy.io.elementParser(element_type, space)

            parsed_element.append(class_init(nodes))
        
        return np.array(parsed_element) #create array of elements
    
    def set_essentials(self, essential_bcs : list):
        """
        This functions sets the essentials conditons to build the problem
        """
        # Initialize the numer array
        for bc in essential_bcs:
            pass

    def __init__(self, name : str, components: list):
        self.name = name
        self.components = components
        
        # initialize list of domains and bondaries
        self.domains = dict()
        self.boundaries = dict()
    



def main():
    pass

if __name__ == "__main__":
    main()