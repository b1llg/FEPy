import os
import numpy as np
from node import Node
from element import E1LIN,E1QUD
from boundarycondition import EssentialBc, ImposedBc
import re

class FemData:
    """
    Class that contains all the raw fem data
    """
    def __init__(self, elements: np.array, 
                 nodes: np.array, 
                 essential_bcs: np.array,
                 imposed_bcs: np.array):
        
        self.elements = elements
        self.nodes = nodes
        self.essential_bcs = essential_bcs
        self.imposed_bcs = imposed_bcs

def filePathGenerator(input_file):
     """
     Generate file path for any file, used with input files.
     """
         #https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
     __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
     return os.path.join(__location__,input_file)

def inputReader(input_file):
    """
    Read and parse input files to extract FE data -> 
    """


    with open(filePathGenerator(input_file)) as file:

        print("Input file: {0} => loaded\n".format(input_file))
        print("Reading data from input file...\n")

        # Initialize Finite Element Data Lists
        elements = []
        nodes = []
        essential_bcs = []
        imposed_bcs = []

        # Method inspired by PolymerFEM: https://www.youtube.com/watch?v=8GWLgK9Llv0&t=4s&ab_channel=PolymerFEM
        for line in file:

            line = line.strip()
            
            # Parameter section
            
            if "#" in line: # Comment line
                continue

            elif "*NODE" in line: # Node definition line
                state = 1
                continue

            elif "*ELEMENT" in line: # Element definition line
                state = 2
                continue

            elif "*BOUNDARY_ESSENTIAL" in  line: # Essential Boundary Condition
                 state = 3
                 continue
            
            elif "*BOUNDARY_IMPOSED" in line:  # Imposed Boundary Condition
                 state = 4
                 continue
                 
            # Data extraction section

            elif state == 1: # Parse node
                nodes.append(nodeParser(line))

            elif state == 2: # Parse element
                elements.append(elementParser(line))

            elif state == 3: # Essential Boundary Condition
                 essential_bcs.append(boundaryConditionParser(line))

            elif state == 4: # Imposed Boundary Condition
                 imposed_bcs.append(boundaryConditionParser(line))
            else:
                raise Warning("Unknown definition: {0}".format(line))
            

    print("Done reading => {0}!\n".format(input_file))
    # print(nodes)
    # print(elements)
    # print(essential_bcs)
    # print(imposed_bcs)


    return FemData(np.array(elements),
                   np.array(nodes),
                   np.array(essential_bcs),
                   np.array(imposed_bcs))

    # Print element statistics

def nodeParser(line):
        
    data = re.findall(r'\d+',line)
    
    return Node(data[0], data[1], data[2], data[3])
        
def elementParser(line):

    pattern = re.compile(r'\s*([A-Za-z0-9]+|\d+)\s*')

    data = pattern.findall(line)
    
    if data[0] == "E1LIN":
            return E1LIN(data[1], np.array([data[2], data[3]]))
    
    elif data[0] == "E1QUD":
            return E1QUD(data[1], np.array([data[2], data[3], data[4]]))
    else:
        raise TypeError("Element {0} not implemented, check documentation".format(data[1]))

def boundaryConditionParser(line):
    """
    Given a line from input files, generate either a EssentialBc or ImposedBc
    """
    pattern = re.compile(r'\s*([A-Za-z0-9]+|\d+)\s*')

    data = pattern.findall(line)

    
    if data[0] == "ESSENTIAL":
         return EssentialBc(data[1], np.array([data[2:]]))
    else:
         return ImposedBc(data[0], data[1:] )

def main():
    pass
    

if __name__ == "__main__":
    main()