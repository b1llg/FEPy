import os

import numpy as np

import fepy.boundary
import fepy.io
import fepy.node
import fepy.space 



class Field:
    """
    A FEM function is either a trial or test function 
    """
    def set_element(self,fem_data: fepy.io.FemData, space: fepy.space.Space):
        """
        Convert the basic raw data to the correct element formulation
        depending on the function space provied

        fem_data: raw fem_data extracted from the generated mesh file

        sapce: function space associated to the current field behind builded
        """
        parsed_element = []
        
        for element_type, element_content in fem_data.elements.items():

            # exclude element types that are empty
            if  len(element_content) > 0:

                # for each element of the current type, use class_init which calls the
                # good initializer for the current type -> fepy.element
                # special case for vertex 
                if element_type == 'vertex':
                    for node in element_content:
                        parsed_element.append(fepy.node.Node(fem_data.nodes[node][0],
                                                             fem_data.nodes[node][1],
                                                             fem_data.nodes[node][2]))
                else:
                    """
                    ***************************************************
                    ***************************************************
                    ***************************************************

                    Try a way with gmsh data to decouple bcs data and 
                    plain volume data. Because things are going to get 
                    parsed multiple times

                    ***************************************************
                    ***************************************************
                    ***************************************************

                    """
                    # get the type of space function
                    class_init = fepy.io.elementParser(element_type, space)

                    for nodes in element_content:
                        parsed_element.append(class_init(nodes))
        
        self.elements = np.array(parsed_element) #create array of elements for the field

    def __init__(self, name : str, components: list):
        self.name = name
        self.components = components

class Model:
    """
    A Model is what we are trying to solve:
    input_file: name of the gmsh file (.geo extension) with full path
    field_array: array of all the fields to be solved
    space_array: array of all the space associated to each field
    """
    def set_fields(self,
                   fem_data: fepy.io.FemData,
                   field_array: list, 
                   space_array: list):
        """
        This functions parses the femdata and create element data for each fields and
        parses the domain and add the correct domains to the correct type:
            vertex
            line
            surface
            specific volume

        also adds the correct element to the correct boundary
        """
        # Set the fields
        for field, space in zip(field_array, space_array):

            # Call set element function
            field.set_element(fem_data, space)

        self.fields = field_array # assign fields to model

        # Set the domains, for now simply takes the data from fem_data
        self.domains = fem_data.domains

        # set the total number of dofs
        self.dofpn = 0
        for field in  self.fields:
                self.dofpn += len(field.components)

        self.tdof = len(self.nodes) * self.dofpn

    def set_domains(self, fem_data : fepy.io.FemData):
        """
        Add boundaries to the model, not itialized yet
        """
        for domain, els in fem_data.domains.items():
            self.domains.append(fepy.boundary.Boundary(domain, els))

    def __init__(self, input_file: str, 
                 field_array : list, 
                 space_array : list):
        
        if len(field_array) != len(space_array):
            raise ValueError("Field size is not the same size a space size")
        
        #Determine highest order
        order = 0
        for s in  space_array:
            # Loop over model spaces, determine equivalent order to generate adequate mesh
            if s.fetype.equiv_order(s.order) > order:
                order = s.fetype.equiv_order(s.order)

        # The reason behind chosing the highest equivalent order is to minimise the mesh file size and mesh data size.
        # After behind genereted and parsed, the correct element formulation will be applied to the element in the correct field.
        # Thus, only one mesh is generated and each element is added to its respected field. Then, each field will add it's contribution
        # to the equation beeing solved
                
        # generate mesh
        mesh_file = fepy.io.meshGen(input_file, order)

        # get raw data from input file
        fem_data = fepy.io.inputReader(mesh_file) 


        # assign node
        self.nodes = fem_data.nodes

        # Now that the data is parsed, each field should have its own element data
        self.set_fields(fem_data, field_array, space_array)

        # initialize domains
        self.domains = []
        self.set_domains(fem_data)
     
    def set_essentials(self, essential_bcs : list):
        """
        This functions sets the essentials conditons to build the problem
        """
        # Initialize the numer array
        for bc in essential_bcs:
            pass


def main():
    pass

if __name__ == "__main__":
    main()