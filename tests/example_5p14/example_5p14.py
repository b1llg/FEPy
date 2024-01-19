import os

import numpy as np

from fepy.core import Field, Model

def main():
    """
    Test a basic case of a loaded cable. From [Les éléments finis de la théorie à la pratique]()
    """

    # Create a 1d displacement field
    u = Field("displacement",np.array(["u"]))

    # read model data and assign displacement field
    print(os.getcwd())
    model = Model("example_5p14.txt", np.array([u]))

    print(model.tdofs)
    # fem_data.SetTotalDofs()

    # print(fem_data.tdof)

if __name__ == "__main__":
    main()
