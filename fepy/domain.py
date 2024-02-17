"""
This module is for boundary conditons
"""
import fepy.element
import fepy.io
import fepy.node
import fepy.space

class Domain:
    """
    This class defines domains. Domains are sets of element on which we integrate to
    build the problem
    """
    def __init__(self):
        self.is_initialized = False # this value changes when the boundary is assigned
        self.elements = dict()

    def add_elements(self, element_data):
        """
        Called from field, add element type and elements to the domain
        """
        for eltype, elements in element_data.items():
            self.elements[eltype] = elements
        
        self.is_initialized = True
    

class Boundary(Domain):
    """
    This class stores boundary data inhertis from domain.

    Each enty has a name and corresponding element
    """
    pass
