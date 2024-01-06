import os
import numpy as np
from node import Node
from element import E1LIN
import re

def InputParser(input_file):

    #https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__,input_file),"r") as file:

        print("Input file: {0} => loaded\n".format(input_file))
        print("Reading data from input file...\n")

        # Initialize Finite Element Data Lists
        elements = []
        nodes = []
        bc = []

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

            elif "*BOUNDARY_CONDITION" in line:
                 state = 3
            
            elif "*LOAD" in line:
                 state = 4
                 
            # Data extraction section

            elif state == 1: # Parse node
                nodes.append(NodeParser(line))

            elif state == 2: # Parse element
                elements.append(ElementParser(line))
            else:
                raise Warning("Unknown definit: {0}".format(line))

    print("Done reading => {0}!\n".format(input_file))

    # Print element statistics

def NodeParser(line):
        
        data = re.findall(r'\d+',line)
        
        return Node(data[0], data[1], data[2], data[3])
        

def ElementParser(line):

        pattern = re.compile(r'\s*([A-Za-z0-9]+|\d+)\s*')

        data = pattern.findall(line)
        
        if data[1] == "E1LIN":
             return E1LIN(np.array([data[2], data[3]]))
        
        # elif data[1] == "E1QUD":
        #      pass
        else:
            raise TypeError("Element {0} not implemented, check documentation".format(data[1]))

def BoundaryConditionParser(line):
     pass


def main():
    InputParser("input.txt")

if __name__ == "__main__":
    main()