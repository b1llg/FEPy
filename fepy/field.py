import os

import numpy as np

import fepy.domain
import fepy.io
import fepy.space

def set_boundaries(self, fem_data: fepy.io.FemData, space: fepy.space.Space):
    """
    Add boundary definition. Loop over fem_data and check boundaries defined in file and add them
    to their respective boundary in field obejct
    """
    for domain in fem_data.domains:
        pass

      
class Field:
    """
    A FEM function is either a trial or test function 
    """
    def add_domain(self,domain: fepy.domain.Domain):
        self.domains[domain] = fepy.domain.Domain()

    def add_boundary(self, boundary : str):
        self.boundaries[boundary] = fepy.domain.Boundary()

    def __init__(self, name : str, components: list):
        self.name = name
        self.dofpn = len(components)
        self.components = components
        
        # initialize list of domains and bondaries
        self.domains = dict()
        self.boundaries = dict()
        self.essentials = []

    def set_spaces(self, space_array : fepy.space.Space ):
        for space in space_array:
            self.space = space

    def set_domains(self, femdata : fepy.io.FemData):
        """
        Assign element data to the correct comain
        """
        #check if the domain called in is part the field domains
        for domain in self.domains:
            if domain in femdata.domains: # Add the domain data to the corresponding domain
                self.domains[domain].add_elements(femdata.domains[domain]) 
            else:
                raise ValueError("Domain {0} not found in {1}".format(domain, femdata))
            

        # Repeat the process for boundaries
        for boundary in self.boundaries:
            if boundary in femdata.domains: # Add the domain data to the corresponding domain
                self.boundaries[boundary].add_elements(femdata.domains[boundary]) 
            else:
                raise ValueError("Boundary {0} not found in {1}".format(boundary, femdata))
        print("test")

        
    
    def set_essentials(self, essential_bcs : list):
        """
        This functions sets the essentials conditons to build the problem
        """
        # Initialize the numer array
        for bc in essential_bcs:
            if bc not in self.essentials:
                self.essentials.append(bc)
            else:
                raise Warning("Can't add {0} to essentials, already added".format(bc))
        
def main():
    pass

if __name__ == "__main__":
    main()