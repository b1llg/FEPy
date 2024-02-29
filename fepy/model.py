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

        self.dofpn = int(self.ndof/self.nnodes)

        # Build the "numer" table -> Table containing the links between each node and each dof
        self.set_numer()

        # "Build" the connec table, in reality it's just assigning dofs to the element
        self.set_connec()

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

        # Number of nodes
        nnodes = len(self.nodes)

        # Generate numer
        self.numer = -1*np.ones((nnodes, self.dofpn),dtype=int)

        # loop over the numer table and assign a dof number to each empty dof of each node
        # each field has its own dof per node, the column in numer will depend of the field
        
        dofid = 0 # initialize a dof id to assign to each empty dof of numer
        nkdof = 0 # number of known dofs
        
        # For each fields generate dofs id but skip essential dofs
        dofcount = 0
        for field, essential in zip(self.fields, essential_list):
            for i in range(dofcount, dofcount + field.dofpn):
                for j in range(self.nnodes):
                        if j not in essential:
                            self.numer[j,i] = int(dofid)
                            dofid +=1
            dofcount += field.dofpn

        # Now continue the numbering knowing that all essential dofs are marked
        m,n = self.numer.shape

        # Fill the remaining (known dofs id). Go column wise so the numbering respect the dofs generation order
        for i in range(n):
            for j in range(m):
                if self.numer[j,i] == -1:
                    nkdof += 1
                    self.numer[j,i] = dofid
                    dofid += 1

        self.nkdof = nkdof
        self.nukdof = self.ndof - self.nkdof

    def set_connec(self):
        """
        This function assigns the dofs to the elements
        """
        # Add dofs to element
        for eltype, elements in self.elements.items():
            for element in elements:
                for node in element.nodes:
                    element.add_dofs(self.numer[node])
                
                # Compute element ndof
                element.ndof = len(element.dofs)

       

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
        self.ndof = 0 # initialize dof per node

        for field in  self.fields:
                self.ndof += field.dofpn

        self.ndof = len(self.nodes) * self.ndof
    