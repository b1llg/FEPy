# import fepy
# import gmsh
import os
import meshio

# read mesh file

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))

input_file = "example_5p14.msh"
mesh = meshio.read(os.path.join(__location__,input_file))

print(mesh)



