import numpy as np
import scipy.linalg
import scipy.sparse 
import scipy.sparse.linalg
import matplotlib.pyplot as plt
import time


from fepy.mesh.parser import msh_parse
from fepy.quadrature import gauss_quad
from fepy.interp import shape_dshape



def main():

    msh_parse("example_5p14.msh")

    ####
    #
    #   Problem definition
    #
    ####
    start_time = time.perf_counter()
    coor = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2.5, 0, 0],
        [3, 0, 0],
        [3.5, 0, 0],
        [4, 0, 0],
        [4.5, 0, 0],
        [5, 0, 0],
    ])

    connec = np.array([
        [0, 0, 2, 1],
        [1, 2, 4, 3],
        [2, 4, 6, 5],
        [3, 6, 8, 7]
    ])

    numer = np.array([
        [0, 7],
        [1, 0],
        [2, 1],
        [3, 2],
        [4, 3],
        [5, 4],
        [6, 5],
        [7, 6],
        [8, 8]
    ])

    adres = np.array([
        [0, 7, 1, 0],
        [1, 1, 3, 2],
        [2, 3, 5, 4],
        [3, 5, 8, 6]
    ])

    ####
    #
    #   Parameters
    #
    ####
    dim = 1         # Dimension of the problem
    nel = 4         # number of element
    nnode = 9       # Number of node
    mgk = 2         # 2 gauss point
    ndk = 3         # Number of dof per element
    nck = 3         # Number of calculation point per element
    eltype = "E1QD"  # Element type

    # Problem
    nkd = 2     # Number of known dof
    nud = 7     # Number of unknown dof
    ndof = nkd + nud

    A = np.zeros((ndof, ndof))
    U = np.zeros((ndof))
    F = np.zeros((ndof))
    S = np.zeros((ndof))

    def f(ksi, x1k, x2k, hk):
        x = ((x1k + x2k) + hk*ksi)/2

        if x >= 0 and x <= 2:
            return -6-40*x
        elif x > 2 and x <= 5:
            return -6
        else:
            ValueError("x should be between 0m and 5m")

    T = 400     # N - tension in cable

    ####
    #
    #   Assembly of the system
    #
    ####

    # Only one type of element, certain functions can be called before the loop to save on
    # computation time

    ksi, w = gauss_quad(mgk)

    end_time = time.perf_counter()
    tinit = end_time - start_time

    start_time = time.perf_counter()
    for k in range(nel):  # Loop on elements

        # Get node number
        n1 = connec[k, 1]
        n2 = connec[k, 2]

        # Get element geometric node position
        x1k = coor[n1, 0]
        x2k = coor[n2, 0]

        # Compute element characteristic length
        hk = x2k - x1k

        # initialize elemental matrices
        aij = np.zeros((ndk, ndk))
        fi = np.zeros((ndk))

        for gp in range(mgk):
            N, B = shape_dshape(eltype, ksi[gp])
            aij += 2*T/hk * np.outer(B, B) * w[gp]
            fi += hk/2 * f(ksi[gp], x1k, x2k, hk) * N * w[gp]

        for d1 in range(0, ndk):  # Loop on dofs
            # Must add 1 to d1 because first column of adres is element #
            i = adres[k, d1+1]  # outter dof

            F[i] += fi[d1]

            for d2 in range(0, ndk):  # Inner dof
                # Must add 1 to d2 because first column of adres is element #
                j = adres[k, d2+1]

                A[i, j] += aij[d1, d2]

    # Boundary conditions
    d1 = 0  # first dof of last element is where the load is applids
    k = 3  # last element
    i = adres[k, d1+1]  # outter dof
    S[i] = -150

    # # Debug matrix entries
    # plt.matshow(A)
    # plt.show()

    end_time = time.perf_counter()
    tassy = end_time - start_time

    ####
    #
    #   System partioning for efficient solving
    #   1) m11*duI = f1c + s1C -> solve(m11, f1c + s1C)
    #   2) Si = m21*duI - f2c
    ####
    start_time = time.perf_counter()
    
    M11 = A[0:nud, 0:nud]

    M21 = A[nud:ndof, 0:nud]

    F1c = F[0:nud]
    S1c = S[0:nud]
    F2c = F[nud:ndof]
    duC = U[nud:ndof]



    # Sparse solve
    M11 = scipy.sparse.csc_matrix(M11) #
    duI = scipy.sparse.linalg.spsolve(M11, F1c+S1c)
    SIu = np.inner(M21, duI) - F2c
    end_time = time.perf_counter()
    tsp = end_time - start_time



    print("\n**********************")
    print("Solving completed, performance:\n")
    print("\tInitialisation: {:.4e} s".format(tinit))
    print("\tAssembly: {:.4e} s".format(tassy))
    print("\tSparse solve: {:.4e} s".format(tsp))
    print("**********************\n")
    ####
    #
    #   Post process
    #
    ####

    # # initialize deflection plot
    # fig, ax = plt.subplot()

    # for k in range(nel):
    #     # for every element get nodes
    #     nodes = connec[k, 1:]

    #     for node in nodes:
    #         ax.scatter()


if __name__ == "__main__":
    main()
