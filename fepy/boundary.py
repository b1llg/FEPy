"""
This module is for boundary conditons
"""
import fepy.element
import fepy.io
import fepy.node

class Boundary:
    """
    This class stores boundary data.

    Each enty has a name and corresponding element
    """
    def __init__(self, name : str, elements: dict):
        self.name = name
        self.elements = elementparser