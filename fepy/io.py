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

    # Retrieve element data
    raw_elements = dict()
    # 0d element
    raw_elements['vertex'] = []

    # 1d elements
    raw_elements['line'] = []
    raw_elements['line3'] = []

    # 2d elements

    # 3d elements


    for cells in mesh.cells:

        # since arrays are inside arrays. Must use a list comprehension to extract all levels
        # of possible data in each type of cells
        match cells.type:
            case 'vertex':
                [raw_elements['vertex'].append(arr) for arr in cells.data[0]]

            case 'line':                 
                [raw_elements['line'].append(arr) for arr in cells.data]

            case 'line3':
                [raw_elements['line3'].append(arr) for arr in cells.data]
           
            case _:
                raise ValueError("cell type {0} invalid, check geo file for possible error leading to a error in .msh file". format(cells.type))
  
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

    # Update 
            
    # parse elements as geometric entities
    """
    **********************************
    Parse elements

    cell_sets refer to the element id from a certain type
    
    mesh.cell_sets_dict['loaded_section_const'] ->    {'line3': array([1, 2, 3], dtype=uint64)}

    mesh.cells_dict['line3'][1] -> array([1, 5, 6])
    **********************************
    """
    print("Nodes content: ")
    print("====================================")
    for node in nodes:
        print("\t" + str(node))

    print("Element content: ")
    print("====================================")
    for eltype, elcont in  raw_elements.items():
        print(eltype)

        for item in elcont:
            print("\t" + str(item))

    print("Domain content: ")
    print("====================================")
    for domain, domain_content in domains.items():
        print(domain)
        
        for eltype, elcont in domain_content.items():
            print("\t" + str(eltype))
            print("\t\t" + str(elcont))
   


    # return    
    elements = []      

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