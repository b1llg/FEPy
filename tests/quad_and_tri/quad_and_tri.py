import os

import numpy as np

from fepy.core import Field, Model
from fepy.space import Space, Lagrangian

def main():
    """
    Test to determine how different element types are stored
    """

    # # Create a 1d displacement field
    u = Field("displacement",np.array(["u"]))

    s = Space(Lagrangian,2)

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "quad_and_tri")

    model = Model(path, np.array([u]), np.array([s]))

    # print(model.tdofs)

if __name__ == "__main__":
    main()