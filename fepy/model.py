import numpy as np

import fepy.io

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

            # Call set functions
            field.set_domain(fem_data, space)
            field.set_boundaries(fem_data, space)
            
        self.fields = field_array # assign fields to model

            # call set_domains


        # set the total number of dofs
        self.dofpn = 0 # initialize dof per node
        for field in  self.fields:
                self.dofpn += len(field.components)

        self.tdof = len(self.nodes) * self.dofpn


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
        
    