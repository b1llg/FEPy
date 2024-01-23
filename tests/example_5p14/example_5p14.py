import os

import numpy as np

from fepy.core import Field, Model
from fepy.space import Space, Lagrangian

def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """

    # # Create a 1d displacement field
    u = Field("displacement",["u"])

    # Initialize function of type Lagrangian order 2 to solve the problem.
    # The problem is still in H1 but we use H2 functions.
    s = Space(Lagrangian,2)

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "example_5p14")

    model = Model(path ,[u], [s])

    # print(model.tdofs)

if __name__ == "__main__":
    main()
