from abc import ABC, abstractmethod

class FEtype(ABC):
    """
    defines type of finite element
    """
    
    @abstractmethod
    def equiv_order(order: int):
        """
        This abstract property serves as bridge between the element family and the gmsh order that suits best the element type
        For example some fluid element have only one node in the center for the pressure, while gmsh elements with node in center are often of higher degree
        """
        pass

class Lagrangian(FEtype):
    """
    defines Lagrangians finite element type
    """

    def equiv_order(order : int):
        return order

class Hermite(FEtype):
    """
    Defines Hermite finite element type
    """
    def equiv_order(order : int):
        return order
    
class MINI(FEtype):
    """
    Defines MINI finite element type for coupled problem
    """
    def equiv_order(order: int):

        if order == 1: # Means order 3 in gmsh
            return 3
        else:
            raise ValueError("Order {0} doesn't exist for MINI element, maximum order 1".format(order))
        
class Space:
    """
    Defines the finite element type part of the desired fe space and calls the appropriate order in mesh generation
    """
    def __init__(self, fetype = Lagrangian, order = 1):
        """
        Initialize a finite element space for the model:
        input:  fetype: Type of finite element (LagrangianFE as default)
                order: order of the polynomials (1 as default)
        """
        self.fetype = fetype
        self.order = order