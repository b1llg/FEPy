
import numpy as np

from fepy.core import Field, Model

def main():
    u = Field("u",np.array(["u"]))

    model = Model("input.txt", np.array([u]))

    print(model.tdofs)
    # fem_data.SetTotalDofs()

    # print(fem_data.tdof)

if __name__ == "__main__":
    main()
