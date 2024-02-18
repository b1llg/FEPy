import numpy as np

import fepy.io

class Model:
    """
    A Model is what we are trying to solve:
    input_file: name of the gmsh file (.geo extension) with full path
    field_array: array of all the fields to be solved
    space_array: array of all the space associated to each field
    """
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

        # set element data
        self.nodes = fem_data.nodes
        self.nnodes = len(self.nodes)
        self.elements = fem_data.elements

        self.set_fields(fem_data, field_array, space_array)

        self.dofpn = int(self.tdof/self.nnodes)

        # Build the "numer" table -> Table containing the links between each node and each dof
        self.set_numer()

        print("test")

    def set_numer(self):
        """
        This function goes through the list of bcs and set the dof number to each node
        """
        # First we need to know what type of elements that used and dimensions.
        problem_dim = 0

        for eltype in self.elements:
            if len(self.elements[eltype]) > 0 and eltype != 'vertex':
                match eltype:
                    case 'line':
                        problem_dim = 1
                    case 'line3':
                        problem_dim = 1
                    case _:
                        raise TypeError("Cannot determine problem dimension from element type: {0}".format(eltype))
        
        if problem_dim == 0:
            raise Warning("Problem Dimension is set to 0, make sure to have appropriate elements for the problems")



        # Retrieve nodes that have an essential bondary conditions, operated only on nodes
        essential_list = []

        for field in self.fields:
            node_list = [] # reset node list before each field essential generation
            for essential in field.essentials:
                # retrieve vertex ids
                vertices = field.boundaries[essential].elements['vertex']

                # from elements, retrieve nodes
                for vertex in vertices:
                    node_list.append(self.elements['vertex'][vertex].nodes[0])

            # for each field, append each node_list, will match the order the fields have been passed
            essential_list.append(node_list)

        # Generate an empty numer 
        nnodes = len(self.nodes)

        self.numer = -1*np.ones((nnodes, self.dofpn))
        # loop over the numer table and assign a dof number to each empty dof of each node
        # each field has its own dof per node, the column in numer will depend of the field
        
        dofid = 0 # initialize a dof id to assign to each empty dof of numer
        
        # For each fields

        flat_essential = [item for sublist in essential_list for item in sublist]
        """
        ******* COntinu here
        
        """
        for field in self.fields:
            for i in range(field.dofpn):
                for j in range(self.nnodes):
                    if self.nodes[j] not in flat_essential:
                        self.numer[j,i] = dofid
                        dofid +=1

        print(self.numer)



       

    def set_fields(self,
                   fem_data: fepy.io.FemData,
                   field_array: list, 
                   space_array: list):
        """
        This functions assign elements to fields and their corresponding boundary
        """
        # Set the fields
        for field, space in zip(field_array, space_array):
            # Call set functions
            field.set_domains(fem_data, space)
            
        self.fields = field_array # assign fields to model
        self.nfields = len(field_array)

 
        # set the total number of dofs
        self.tdof = 0 # initialize dof per node

        for field in  self.fields:
                self.tdof += field.dofpn

        self.tdof = len(self.nodes) * self.tdof
    