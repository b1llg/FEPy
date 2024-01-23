// Geomtetry definition

// Square
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

// Boundaries square
Physical Curve("bc_essential_s") = {4};
Physical Point("bc_load_s") = {2};
Physical Surface("volume_s") = {1};

// tri
Point(5) = {2.0, 0.0 , 0.0};
Point(6) = {3.0, 0.0 , 0.0};
Point(7) = {2.5, 1.0 , 0.0};

Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,5};

Curve Loop(2) = {5,6,7};

Plane Surface(2) = {2};

// Boundaries triangle
Physical Curve("bc_essential_t") = {5};
Physical Point("bc_load_t") = {7};
Physical Surface("volume_t") = {2};





