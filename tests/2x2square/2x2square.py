import os

import numpy as np

from fepy.core import Field, Model
from fepy.space import Space, Lagrangian

def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """

    # # Create a 1d displacement field
    u = Field("displacement",np.array(["u"]))

    s = Space(Lagrangian,1) # H2

    # read model data and assign displacement field
    path = os.path.join(os.path.dirname(__file__), "2x2square")

    model = Model(path, np.array([u]), np.array([s]))

    # print(model.tdofs)

if __name__ == "__main__":
    main()