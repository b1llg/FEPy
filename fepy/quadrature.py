import numpy as np


def gauss_quad(mgk):
    """
    Gauss quadrature on 1d elements:
    This function returns ksi and w for 'mgk' gauss point
    """
    match mgk:
        case 1:
            ksi = np.array([0])
            w = np.array([2])

        case 2:
            ksi = np.array([-0.577350269189625,
                            0.577350269189625])

            w = np.array([1,
                          1])
        case 3:
            ksi = np.array([-0.774596669241483,
                            0.0,
                            0.774596669241483])

            w = np.array([0.555555555555556,
                          0.888888888888889,
                          0.555555555555556])

        case 4:
            ksi = np.array([-0.861136311594052,
                            -0.339981043584856,
                            0.339981043584856,
                            0.861136311594052])

            w = np.array([0.347854845137454,
                          0.652145154862545,
                          0.652145154862545,
                          0.347854845137454])

        case 5:
            ksi = np.array([-0.906179845938664,
                            -0.538469310105683,
                            0.0,
                            0.538469310105683,
                            0.906179845938664])
            
            w = np.array([0.236926885056189,
                          0.478628670499365,
                          0.568888889888889,
                          0.478628670499365,
                          0.236926885056189])
        case _:
            ValueError("Mgk value of {0} not defined", mgk)

    return [ksi, w]

def main():
    print("Running \"quadrature.py\"")


if __name__ == "__main__":
    main()
