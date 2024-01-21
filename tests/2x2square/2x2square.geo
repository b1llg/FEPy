// Geomtetry definition

Point(1) = {0.0, 0.0, 0.0};
Point(2) = {1.0, 0.0, 0.0};
Point(3) = {1.0, 1.0, 0.0};
Point(4) = {0.0, 1.0, 0.0};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Curve Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

Transfinite Curve{1,2,3,4} = 3;

Transfinite Surface{1} = {1,2,3,4};

Recombine Surface{1};

// // Boundaries
// Physical Curve("bc_essential") = {4};
// Physical Point("bc_load") = {2};
// Physical Surface("volume") = {1};

// // // Set mesh properties
// Mesh.ElementOrder = 2;
// Mesh 2;
// // Mesh.HighOrderOptimize = 2;