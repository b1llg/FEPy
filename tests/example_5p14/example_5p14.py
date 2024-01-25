import os

import numpy as np

from fepy.core import Field, Model
from fepy.space import Space, Lagrangian, Hermite
from fepy.boundarycondition import EssentialBc

def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """

    # # Create a 1d displacement field
    u = Field("displacement",["u"])

      # Initialize function of type Lagrangian order 2 to solve the problem.
    # The problem is still in H1 but we use H2 functions.
    s_u = Space(Lagrangian,2)

    #*********************************************************
    #                   Boundaries
    #
    #   Names must match the ones created in the .geo file
    #
    #*********************************************************

    # Define boundary conditions: fixed boundary at each end
    gamma_u = EssentialBc("BC_Fix", [0])

    # Define point load at x=4
        #todo
    # Define element load on line #1
        #todo

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "example_5p14")

    model = Model(path ,[u], [s_u])
    
    print("test")
    # print(model.tdofs)

if __name__ == "__main__":
    main()
