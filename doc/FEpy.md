# FEPy: Simple Finite Element Solve in Python
## Introduction

FEPy is built to solve simple finite element (FE) problems. The code methodology is based around the book by André Fortin: [Les éléments finis de la théorie à la pratique](https://giref.ulaval.ca/afortin/elements_finis.pdf).

The main goal of FEPy is not be an efficient solve, but rather an easy to understand and easy to modify code to learn FE programming using the above book.

## Finite Element Basics

The goal of FE is to solve a PDE using a weakened form of the equation. Let's take the poisson equation:

$$-\Delta \vec u = \vec f$$ 

with these conditions:


to obtain the weak form, we have to multiply each terms by a weight/test function $w$ and then integrate by parts:

$$\int_{\Omega}\vec w \Delta \vec u d\Omega = \int_{\Omega} \vec w \vec f$$
using divergence theorem we obtain the weak form:

$$\int_{\Omega} \nabla \vec w \nabla \vec u d\Omega + \int_{\Gamma}w\dfrac{\partial u}{\partial \vec n} dS = \int_{\Omega} w f d\Omega $$

($\nabla$: gradient, $\Delta$: Laplacian).

Now, we have to choose a type of function that are differentiable at leat one time since the test function $w$ and the trial function $u$ are both differentiated once &rarr; $\nabla \vec w$ and $\nabla \vec u$. The simplest approach is to select the same function for the trial and test function. This method is called the Ritz method. These function depends on the dimension of the problem. In the case of a 1D problem, line elements are used. In 2D, quads and tris are mostly used. In 3D, tetrahedrals and hexadrals are mostly used. A good reference for elements shape (trial) function is: [Finite Element Method](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118569764). This book contains the definition of shape functions and their derivatives for a wide range of element in 1D, 2D and 3D. It contains a lot of information regarding the FE method and simple Matlab codes.

Once a dimension is selected with its respective function, we can build a linear system to solve. As for the first term in the weak form above, we obtain:
$$\sum_{k}$$
## Input file

The input files are used to 