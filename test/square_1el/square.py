import os
import meshio

# read mesh file

__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))

input_file = "square.msh"
mesh = meshio.read(os.path.join(__location__,input_file))

print(mesh)