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
    # disp = Field("displacement",["u"])
    disp = Field("displacement",["u", "v"])
    temp = Field("temperature",["T"])

    # add domains to the field
  
    disp.add_domain('volume')

    disp.add_boundary('bc_fix')
    disp.add_boundary('loaded_section_ramp')
    disp.add_boundary('load_point')
    disp.add_boundary('loaded_section_const')

    disp.set_essentials(['bc_fix'])

    # # Add domains to the temperature field
    temp.add_boundary('load_point')
    temp.set_essentials(['load_point'])

    # Initialize function of type Lagrangian order 2 to solve the problem.
    # The problem is still in H1 but we use H2 functions.
    # create trial function and weight function, dimensions will match the field it's added to

    s_uw = Space(Lagrangian,2)

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "example_5p14") # since working in /tests, must use complete path as file input

    # Now from the model we have the essential data: elements, nodes and fields
    # model = Model(path ,[disp], [s_uw]) 
    model = Model(path ,[disp, temp], [s_uw, s_uw])   

    # Integration loop


if __name__ == "__main__":
    main()
