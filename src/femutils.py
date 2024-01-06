import os
import numpy as np
from node import Node
import re

def InputParser(input_file):

    #https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__,input_file),"r") as file:
        
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
        

            # Data extraction section

            elif state == 1: # Parse node
                NodeParser(line)

            elif state == 2: # Parse element
                ElementParser(line)


def NodeParser(line):
        
        data = re.findall(r'\d+',line)
        
        return Node(data[0], data[1], data[2], data[3])
        

def ElementParser(line):
        data = re.findall(re.compile(r'\s*(\D+|\d+)\s*'),line)
        
        if data[1] == "E1LIN":
             pass
        elif data[1] == "E1QUAD":
             pass
        else:
            raise TypeError("Element {0} not implemented, check documentation".format(data[1]))

def BoundaryConditionParser(line):
     pass


def main():
    InputParser("input.txt")

if __name__ == "__main__":
    main()