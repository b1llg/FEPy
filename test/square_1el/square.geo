// Geometry definition
Point(1) = {0, 0, 0};
Point(2) = {1, 0, 0};
Point(3) = {1, 1, 0};
Point(4) = {0 ,1, 0};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Curve Loop(1) = {1,2,3,4};

Plane Surface(1) = {1};

// Boundaries definition
Physical Point("BC_Fix") = {1,2};
Physical Curve("Loaded_Section") = {3};

// Transfinite Operation
Transfinite Curve{-1, 3} = 1; 
Transfinite Curve{2, 4} = 1;


Transfinite Surface{1} = {1,2,3,4};

Recombine Surface{1};

// Mesh
Mesh 2;
Mesh.ElementOrder = 1;

// Save Mesh
Save "square.msh";//+
Physical Curve("Loaded_section", 5) = {3};
