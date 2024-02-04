import subprocess

import meshio
import numpy as np 

import fepy.element
import fepy.node
import fepy.space



class FemData:
    """
    Class that contains all the raw fem data
    """
    def __init__(self, 
                 nodes: list, 
                 elements: list, 
                 domains: dict):
        
        self.elements = elements
        self.nodes = nodes
        self.domains = domains

def meshGen(input_file: str, order: int):
    """
    Generate the mesh with gmsh based on the type of element and order
    """
    # check that element order is below a certain treshold to prevent 
    if order > 3:
        raise ValueError("Element order is to high, select element order below 3")    


    # send shell command to generate mesh based on input order
    try:


        # os.system("gmsh {0}.geo -order {1} -3".format(input_file,order))
        subprocess.run(["gmsh", "{0}.geo".format(input_file), "-order", "{0}".format(order), "-3"],
                       capture_output= False,
                       check=True,
                       stdout=subprocess.DEVNULL
                       )

        # if no error, return msh file
        return input_file + ".msh"

    except:
        raise SystemError("Error while generating mesh")

def inputReader(input_file: str): 
     """
     Call the appropriate appropriate reader depending on the file format
     """
     # extract file format
     file_format = input_file.split(".")[-1]

     if file_format == "msh":
          return gmshParser(input_file)

     else:
         raise ValueError("Unssuported: '.{0}' file format. For now only '.gmsh' format is supported")

def gmshParser(input_file : str):
    """
    Parse gmsh file format input files to generate fe data. 
    """
    # read data in
    mesh = meshio.read(input_file)

    # initialize a node container
    nodes = []

    # Generate node data from meshio object
    for node in mesh.points:
        nodes.append(node)

    """
    **********************************
    Parse elements

    cell_sets refer to the element id from a certain type
    **********************************
    """

    elements = []


            # Extract domain data
    domains = dict()

    for subdomain, subdomain_content in mesh.cell_sets_dict.items():
        if (subdomain not in domains) and ("gmsh" not in subdomain):
            # Create a dictionnary entry for each element type in a boundary
            # get element type
            
            for eltype, items in subdomain_content.items():
                # get item id reference in element list
                els = []
                [els.append(it) for it in items]


                domains[subdomain] = {eltype : els}
            
    # parse elements as geometric entities
    

    # return          
    return FemData(nodes, elements, domains)
    
def elementParser(element_type: str, space = fepy.space.Lagrangian):

    match element_type:
            case 'vertex':
                return fepy.node.Node
            case 'line':                 
                if space.fetype == fepy.space.Lagrangian:
                    return fepy.element.E1L1
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'line3':
                if space.fetype == fepy.space.Lagrangian:
                    return fepy.element.E1L2
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'line4':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'triangle':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'triangle6':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'triangle10':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'quad':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'quad9':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))

            case 'quad16':
                if space.fetype == fepy.space.Lagrangian:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                elif space.fetype == fepy.space.Hermite:
                    raise NotImplementedError("{0} function is not yet implemented for {1} element".format(space.fetype, element_type))
                else:
                    raise TypeError('Element {0} as no formulation {1}, check space assignment'.format(element_type,space.fetype))
            
            case _:
                raise ValueError("Something is wrong here: fepy.io.elementParse. A check has not been done beforehand. Got {0} has element type".format(element_type))


            # to do : 3d elements


def main():
    pass
    

if __name__ == "__main__":
    main()