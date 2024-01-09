from node import *
from femcore import *
from element import *
from ioutils import *

def main():
    fem_data = inputReader("input.txt")

    u = Field("u",np.array(["u"]))

    model = Model(fem_data, np.array([u]))

    print(model.tdofs)
    # fem_data.SetTotalDofs()

    # print(fem_data.tdof)

if __name__ == "__main__":
    main()
