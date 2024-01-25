from abc import ABC, abstractmethod
import numpy as np

from fepy.node import *


class Element(ABC):
    def __init__(self, nodes: np.ndarray):
        self.nodes = self.checkNodes(nodes)
        self.nnodes = self.nodes.size

    def connect(self, connec_array: np.array):
        self.connectivity = connec_array
        
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

    @abstractmethod
    def checkNodes(self, nodes):
        pass

class E1L1(Element):
    """
    1d Lagrange 1st order element
    """

    @property
    def ndof(self):
        return 2

    def N(self, gp: np.ndarray):
        return np.array([1-gp[0], gp[0]])
    
    def B(self, gp: np.ndarray):
        return np.array([1, -1])
    
    def checkNodes(self, nodes: np.array) -> np.ndarray:
        if not isinstance(nodes, np.ndarray):
            raise TypeError("Nodes should be of type np.array: {0} is beeing used".format(str(type(nodes))))
        elif nodes.size != 2:
            raise ValueError("E1LIN requires 2 nodes, {0} nodes has been passed".format(nodes.size))
        return nodes
    
    
    
class E1L2(Element):
    """
    1d Lagrange 2nd order element
    """

    @property
    def ndof(self):
        return 3
    
    # @property
    # def connec(self):
    #     return self.connectivity

    # @property
    # @abstractmethod
    # def connec(self, connec_array: np.array):
    #     self.connectivity = connec_array


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
            raise ValueError("E1QUD requires 3 nodes, {0} nodes has been passed".format(nodes.size))
        return nodes
    

def main():
    # Create an E1LIN
    n1 = Node(0,0,0)
    n2 = Node(1,0,0)
    n3 = Node(0.5,0,0)


    print("E1L1: ")
    e1 = E1L1(1, np.array([n1,n2]))

    e1.connect(np.array([1,2]))

    print("ndof: ",e1.ndof)

    print("Connectivity: ", e1.connectivity)

    print("nnodes: ",e1.nnodes)

    print("N(0.3): ",e1.N(np.array([0.3])))

    print("\n")

    print("E1L3: ")
    e2 = E1L1(2, np.array([n1,n2,n3]))

    print("ndof: ",e2.ndof)

    print("nnodes: ",e2.nnodes)

    print("N(0.3): ",e2.N(np.array([0.3])))

if __name__ == "__main__":
    main()
