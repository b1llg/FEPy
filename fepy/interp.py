import numpy as np


def main():
    pass


def shape_dshape(eltype, ksi):
    """
    shape_shape: shape function and their derivative
    ****IMPORTANT:
        Must reflect correct node numbering
    """
    if eltype == "E1QD":
        shape = 0.5 * np.array([-ksi*(1-ksi),
                                ksi*(1+ksi),
                                2*(1-ksi*ksi)
                                ])
        
        dshape = 0.5 * np.array([-1+2*ksi,
                                 1+2*ksi,
                                 -4*ksi
                                ])
    else:
        TypeError("element type not defined")

    return [shape, dshape]


if __name__ == "__main__":
    main()
