Lx = 1200;
Ly = 2200;
h = 0.1;
hx = 20;
hy = 10;
Point(1) = {0, 0, 0};
Point(2) = {Lx, 0, 0};
Point(3) = {Lx, Ly, 0};
Point(4) = {0, Ly, 0};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(5) = {1, 2, 3, 4};
Plane Surface(6) = {5};

// Transfinite Curve {1, 3} = Lx/hx + 1 Using Progression 1;
// Transfinite Curve {5, 10, 11, 12} = Ly/hy + 1 Using Progression 1;
Transfinite Curve {1, 3} = 60 + 1 Using Progression 1;
Transfinite Curve {2, 4} = 220 + 1 Using Progression 1;
Transfinite Surface {6};
Recombine Surface {6};

