import os

import numpy as np

from fepy.domain import Boundary, Domain
from fepy.field import Field
from fepy.model import Model
from fepy.space import Space, Lagrangian



def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """
    # # Create a 1d displacement field
    disp = Field("displacement",["u"])
    # disp = Field("displacement",["u", "v"])
    # temp = Field("temperature",["T"])

    # add domains to the field
  
    disp.add_domain('volume')

    disp.add_boundary('bc_fix')
    disp.add_boundary('loaded_section_ramp')
    disp.add_boundary('load_point')
    disp.add_boundary('loaded_section_const')

    disp.set_essentials(['bc_fix'])

    # # Add domains to the temperature field
    # temp.add_boundary('load_point')
    # temp.set_essentials(['load_point'])

    # Initialize function of type Lagrangian order 2 to solve the problem.
    # The problem is still in H1 but we use H2 functions.
    # create trial function and weight function, dimensions will match the field it's added to

    s_uw = Space(Lagrangian,2)

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "example_5p14") # since working in /tests, must use complete path as file input

    # Now from the model we have the essential data: elements, nodes and fields
    model = Model(path ,[disp], [s_uw]) 
    # model = Model(path ,[disp, temp], [s_uw, s_uw])   

    #==============================================================
    #
    #                       Problem loop
    #
    #==============================================================

    # Global
    A = np.zeros((model.ndof, model.ndof))        # Stiffness matrix
    U = np.zeros(model.ndof)                    # Displacement vector
    F = np.zeros(model.ndof)                 # Primary load vector
    S = np.zeros(model.ndof)                 # Secondary load vector

    # Problem partionning
    M11 = np.zeros((model.nkdof, model.nkdof))    # Partitions of stiffness matrix
    M12 = np.zeros((model.nkdof, model.nukdof))
    M21 = np.zeros((model.nukdof, model.nkdof))
    M22 = np.zeros((model.nukdof, model.nukdof))

    Duk = np.zeros(model.nukdof)              # Vector of known displacement
    Duu = np.zeros(model.nukdof)              # Vector of unknown displacement

    F1k = np.zeros(model.nkdof)              # Vector of Primary loads 1
    F2k = np.zeros(model.nukdof)              # Vector of Primary loads 2
    Sk = np.zeros(model.nkdof)                # Vector of Secondary loads 1
    Su = np.zeros(model.nukdof)               # Vector of Secondary loads 2



    # Volume loop - Solid mechancis
    field_loc = 0
    for eltype, elements in model.fields[field_loc].domains['volume'].elements.items():
        for element in elements:
            aij = np.zeros(model.elements[eltype][element].dofs[field_loc])
        pass


if __name__ == "__main__":
    main()
