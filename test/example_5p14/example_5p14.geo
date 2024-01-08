// GMSH project: example_5p14
// Geomtetry definition

Point(1) = {0.0, 0.0, 0.0};
Point(2) = {2.0, 0.0, 0.0};
Point(3) = {4.0, 0.0, 0.0};
Point(4) = {5.0, 0.0, 0.0};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};

Transfinite Curve{1} = 2;
Transfinite Curve{2} = 3;
Transfinite Curve{3} = 2;

// Boundaries
Physical Point("BC_Fix") = {1,4};
Physical Point("Load_Point") = {3};
Physical Curve("Loaded_Section") = {1};

// Set mesh properties
Mesh 1;
Mesh.ElementOrder = 2;

Save "example_5p14.msh";
Save "example_5p14.bdf";
