import os
import numpy as np

def InputParser(input_file):

    #https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__,input_file),"r") as file:
        
        line = file.readline()

        if "*BEGIN" not in line:
            raise ValueError("Input must start with '*BEGIN' keyword")
        
        line = file.readline()

        while "*END" not in line:
            if "*" in line:
                print(line)
            elif("#" in line):
                print(line)
            elif "*NODE" in line:
                print(line)
            elif "*ELEMENT" in line:
                print(line)

            line = file.readline()

        

def NodeParser(file):
    line = file.readline()
    nodes = np.array()

    while "*" not in line:
        line = line.split("\t")


def main():
    InputParser("input.txt")

if __name__ == "__main__":
    main()