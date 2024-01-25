import subprocess

import meshio

import fepy.space
import fepy.element


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

def inputReader(input_file):
     """
     Call the appropriate appropriate reader depending on the file format
     """
     # extract file format
     file_format = input_file.split(".")[-1]

     if file_format == "msh":
          return gmshParser(input_file)

     else:
         raise ValueError("Unssuported: '.{0}' file format. For now only '.gmsh' format is supported")

def gmshParser(input_file):
    """
    Parse gmsh file format input files to generate fe data. 
    """
    # read data in
    mesh = meshio.read(input_file)

    # initialize a node container
    nodes = []

    # Generate node data from meshio object
    for node in mesh.points:
        nodes.append([node[0], node[1], node[2]])

    # Retrieve element data
    vertex = []

    line = []
    line3 = []
    line4 = []

    triangle = []
    triangle6 = []
    triangle10 = []

    quad = []
    quad9 = []
    quad16 = []

    #3d elements


    for cells in mesh.cells:

        # since arrays are inside arrays. Must use a list comprehension to extract all levels
        # of possible data in each type of cells
        match cells.type:
            case 'vertex':
                [vertex.append(arr) for arr in cells.data]

            case 'line':                 
                [line.append(arr) for arr in cells.data]

            case 'line3':
                [line3.append(arr) for arr in cells.data]

            case 'line4':
                [line4.append(arr) for arr in cells.data]

            case 'triangle':
                [triangle.append(arr) for arr in cells.data]

            case 'triangle6':
                [triangle6.append(arr) for arr in cells.data]

            case 'triangle10':
                [triangle10.append(arr) for arr in cells.data]

            case 'quad':
                [quad.append(arr) for arr in cells.data]

            case 'quad9':
                [quad9.append(arr) for arr in cells.data]

            case 'quad16':
                [quad16.append(arr) for arr in cells.data]
            
            case _:
                raise ValueError("cell type {0} invalid, check geo file for possible error leading to a error in .msh file". format(cells.type))


            # to do : 3d elements

    # Create element dict
    elements = dict()

    elements["vertex"] = vertex

    elements["line"] = line
    elements["line3"] = line3
    elements["line4"] = line4

    elements["triangle"] = triangle
    elements["triangle6"] = triangle6
    elements["triangle10"] = triangle10

    elements["quad"] = quad
    elements["quad9"] = quad9
    elements["quad16"] = quad16

    # 3d

    # Extract domain data
    domains = dict()
    for subdomain in mesh.cell_sets_dict.keys():
        if (subdomain not in domains) and ("gmsh" not in subdomain):
            domains[subdomain] = mesh.cell_sets_dict[subdomain]

    # return
    return FemData(nodes, elements, domains)
    
def elementParser(element_type: str, space: fepy.space.Space):

    match element_type:
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