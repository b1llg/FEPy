"""
This module is for boundary conditons
"""
import fepy.element
import fepy.io
import fepy.node
import fepy.space

class Boundary:
    """
    This class stores boundary data.

    Each enty has a name and corresponding element
    """
    def __init__(self, name : str, elements: dict, space : fepy.space.Space):
        self.name = name
        self.elements = fepy.io.elementParser(name, space)