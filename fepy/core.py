import os

import numpy as np

import fepy.io
import fepy.space 


class Field:
    """
    A field is what is studied. 
    - Heat Transfer : Temperature (scalar)
    - Solid Mechanics: Displacement (vector)
    """
    def set_element(self,fem_data: fepy.io.FemData, space: fepy.space.Space):
        """
        Convert the basic raw data to the correct element formulation
        depending on the function space provied

        fem_data: raw fem_data extracted from the generated mesh file

        sapce: function space associated to the current field behind builded
        """
        for element_type in fem_data.elements.keys():
            # Todo: Design map to convert and extract node 
            # Check element parser in fepy.io

            # Dont consider vertex because they are not element types, exclude element types that are empty
            if  not element_type == "vertex" and len(fem_data.elements[element_type]) > 0:

                parsed_elements = fepy.io.elementParser(element_type, fem_data.elements[element_type], space)

                for element in fem_data.elements[element_type]:
                    print(element)

    def __init__(self, name : str, components: list):
        self.name = name
        self.components = components
        self.dof_per_node = len(components)

class Model:
    """
    A Model is what we are trying to solve:
    input_file: name of the gmsh file (.geo extension) with full path
    field_array: array of all the fields to be solved
    space_array: array of all the space associated to each field
    """
    def set_fields(self,
                   fem_data : fepy.io.FemData, 
                   field_array: list, 
                   space_array: list):
        """
        This functions parses the femdata and create element data for each fields.
        """
        for field, space in zip(field_array, space_array):

            # WIP
            field.set_element(self.fem_data, space)


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
        self.fem_data = fepy.io.inputReader(mesh_file) 

        # Now that the data is parsed, each field should have its own element data
        self.set_fields(self.fem_data,  field_array, space_array)




def main():
    pass

if __name__ == "__main__":
    main()