import os

import numpy as np

from fepy.boundarycondition import EssentialBc, LoadBc
from fepy.fem import TrialFunction, WeightFunction, BilinearForm
from fepy.core import Field, Model
from fepy.space import Space, Lagrangian
from fepy.operator import grad, dot



def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """

    # # Create a 1d displacement field and its test function
    disp = Field("displacement",["u"])

    # Initialize function of type Lagrangian order 2 to solve the problem.
    # The problem is still in H1 but we use H2 functions.
    # create trial function and weight function, dimensions will match the field it's added to

    s_uw = Space(Lagrangian,2)

    u = TrialFunction(s_uw)

    w = WeightFunction(s_uw)



    # Define boundary conditions: fixed boundary at each end
    gamma_u = EssentialBc("bc_fix", [0])

    # Define point load at x=4
    gamma_l = LoadBc("load_point", [-150])

    # Define distributed load on line #1
    pload = lambda x : -1*(6+40*x)
    
    gamma_dl1 = LoadBc("loaded_section_ramp", [pload])

    # Define constant load on other elements
    gamma_dl2 = LoadBc("loaded_section_const", [6])

    # Define constant tension
    tension = 400 # N

    # Generate bilinear form from the weak form
    a = lambda  u, w :  tension*grad(u)*grad(w)
    l = lambda pload : pload*w

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "example_5p14") # since working in /tests, must use complete path as file input

    # Now from the model we have the essential data: elements, nodes and fields
    model = Model(path ,[u], [s_uw])

    # Now we add boundary conditions to the model
    model.add_EssentialBc(gamma_u) #.add_LoadBC(gamma_l).add_LoadBC(gamma_dl1).add_LoadBC(gamma_dl2)
    
    print(model)
    # print(model.tdofs)

if __name__ == "__main__":
    main()
