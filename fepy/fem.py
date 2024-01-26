"""
# FEPy.fem

## Intro
This module contains all functions and classes related to the fem classes. Even though
elements are part of the fem theory, they have their own module considering the amount
of functions related to their implementation

## Classes

1. FEMFunction
2. TrialFunction
3. WeightFunction
4. BilinearForm

"""

from abc import ABC

import fepy.space

class FEMFunction(ABC):
    """
    Abstract class to define trial and weight functions
    """
    def __init__(self, space : fepy.space.Space):
        self.space = space

class TrialFunction(FEMFunction):
    """
    Class to define trial functions i.e. what we are trying to solve 
    """
    pass

class WeightFunction(FEMFunction):
    """
    Class to define weight functions i.e. the functions added to generate
    the weak form and that vanishes on boundaries
    """
    pass

class BilinearForm:
    """
    Class that 
    """
    pass

def main():

    s_u = fepy.space.Space() # lagrangian 1st order by default

    u = TrialFunction(s_u)

    print("test")

if __name__ == "__main__":
    main()