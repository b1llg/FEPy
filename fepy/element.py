from abc import ABC, abstractmethod
import numpy as np

import fepy.node


class AbstractElement(ABC):
    """
    Base class for element definition
    """
    def __init__(self, nodes: np.ndarray):
        self.nodes = self.checkNodes(nodes)

    @property
    @abstractmethod
    def nnodes(self):
        pass
    

class GeometricElement(AbstractElement):
    """
    Below are all geometric elements, they contaisn all the geometric data of the
    element and they are all model dependant.
    """
    @property
    @abstractmethod
    def dim():
        pass

    

class Vertex(GeometricElement):
    """
    Class to define nodes as element
    """
    def dim():
        return 0
    
    def nnodes(self):
        return 1

    def checkNodes(self, nodes: np.array) -> np.ndarray:
        if not isinstance(nodes, np.ndarray):
            raise TypeError("Nodes should be of type np.array: {0} is beeing used".format(str(type(nodes))))
        elif nodes.size != 1:
            raise ValueError("Vertex requires 1 node, {0} nodes has been passed".format(nodes.size))
        return nodes

###
# 
#       1D Elements
#   
###
class Line(GeometricElement):
    """
    Class for 2 node line element (1d)
    """
    def dim():
        return 1
    
    @property
    def nnodes(self):
        return 2


class Line3(GeometricElement):
    """
    Class for 3 node line element
    """
    def dim():
        return 1
    
    @property
    def nnodes(self):
        return 3

###
# 
#       2D Elements
#   
###

class Triangle(GeometricElement):
    pass

class Triangle6(GeometricElement):
    pass

class Quad(GeometricElement):
    pass

class Quad9(GeometricElement):
    pass

###
# 
#       3D Elements
#   
###




class FieldElement(AbstractElement):
    """
    Below are all space depent elements, they rely on fields. They retrieve geometric data from the geometric element
    in the model
    """
    @property
    @abstractmethod
    def ndof():
        pass

    @abstractmethod
    def N(self, gp: np.ndarray):
        pass

    @abstractmethod
    def B(self ,gp: np.ndarray):
        pass

class E1L1(FieldElement):
    """
    1d Lagrange 1st order element
    """

    @property
    def ndof(self):
        return 2
    
    @property
    def nnodes(self):
        return 2

    def N(self, gp: np.ndarray):
        return np.array([1-gp[0], gp[0]])
    
    def B(self, gp: np.ndarray):
        return np.array([1, -1])
    
    def checkNodes(self, nodes: np.array) -> np.ndarray:
        if not isinstance(nodes, np.ndarray):
            raise TypeError("Nodes should be of type np.array: {0} is beeing used".format(str(type(nodes))))
        elif nodes.size != 2:
            raise ValueError("E1L1 requires 2 nodes, {0} nodes has been passed".format(nodes.size))
        return nodes
    
    
    
class E1L2(FieldElement):
    """
    1d Lagrange 2nd order element
    """

    @property
    def ndof(self):
        return 3

    @property
    def nnodes(self):
        return 3    

    def N(self, gp: np.ndarray):
        return 0.5*np.array([-gp[0] * (1 - gp[0]), 
                             2 * (1 - gp[0]**2), 
                             gp[0] * (1 + gp[0])])
    
    def B(self, gp: np.ndarray):
        return 0.5*np.array(-1 + 2*gp[0],
                            -4*gp[0],
                            1 + 2*gp[0])
    
    def checkNodes(self, nodes: np.array) -> np.ndarray:
        if not isinstance(nodes, np.ndarray):
            raise TypeError("Nodes should be of type np.array: {0} is beeing used".format(str(type(nodes))))
        elif nodes.size != 3:
            raise ValueError("E1L2 requires 3 nodes, {0} nodes has been passed".format(nodes.size))
        return nodes
   

def main():
    # Create an E1LIN
    n1 = fepy.node.Node(np.array([0,0,0]))
    n2 = fepy.node.Node(np.array([2,0,0]))
    n3 = fepy.node.Node(np.array([1,0,0]))


    print("E1L1: ")
    e1 = E1L1(np.array([n1,n2]))

    print("ndof: ",e1.ndof)
    print("nnodes: ", e1.nnodes)


    # print("N(0.3): ",e1.N(np.array([0.3])))

    # print("\n")

    print("E1L2: ")
    e2 = E1L2(np.array([n1,n2,n3]))

    # print("ndof: ",e2.ndof)

    # print("nnodes: ",e2.nnodes)

    # print("N(0.3): ",e2.N(np.array([0.3])))

    print("Geomtric element: ")
    print("Vertex:")

    e3 = Vertex(np.array([n1]))

    print("test")

if __name__ == "__main__":
    main()
