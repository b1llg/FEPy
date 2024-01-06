from abc import ABC, abstractmethod
from node import *
import numpy as np

class Element(ABC):
    def __init__(self, nodes: np.ndarray):
        self.nodes = self.checkNodes(nodes)
        self.nnodes = self.nodes.size

    @abstractmethod
    def N(self, gp: np.ndarray):
        pass

    @abstractmethod
    def B(self ,gp: np.ndarray):
        pass

    @abstractmethod
    def checkNodes(self, nodes):
        pass

class E1LIN(Element):

    def N(self, gp: np.ndarray):
        return np.array([1-gp[0], 1])
    
    def B(self, gp: np.ndarray):
        return np.array([1, -1])
    
    def checkNodes(self, nodes: np.array) -> np.ndarray:
        if not isinstance(nodes, np.ndarray):
            raise TypeError("Nodes should be of type np.array: {0} is beeing used".format(str(type(nodes))))
        elif nodes.size != 2:
            raise ValueError("E1LIN requires 2 nodes, {0} nodes has been passed".format(nodes.size))
        return nodes
    

def main():
    # Create an E1LIN
    n1 = Node(0,0,0)
    n2 = Node(1,0,0)
    n3 = Node(0.5, 0,0)


    e1 = E1LIN(np.array([n1,n2]))
    print(e1.nnodes)

    print(e1.N())

if __name__ == "__main__":
    main()