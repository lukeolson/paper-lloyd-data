cl = 0.1;

r = 0.8;

//  8-------9    10     11-----12
//  |                           |
//  |        \ _ _7_ _ /        |
//  |                           |
//  |          _ _6_ _          |
//  |        /         \        |
//  1-------2     3     4-------5

// point entities
Point(1)  = {-2, -1, 0, cl};
Point(2)  = {-r, -1, 0, cl};
Point(3)  = { 0, -1, 0, cl};
Point(4)  = { r, -1, 0, cl};
Point(5)  = { 2, -1, 0, cl};
//
Point(6)  = { 0, -1+r, 0, cl};
Point(7)  = { 0,  1-r, 0, cl};
//
Point(8)  = {-2,  1, 0, cl};
Point(9)  = {-r,  1, 0, cl};
Point(10) = { 0,  1, 0, cl};
Point(11) = { r,  1, 0, cl};
Point(12) = { 2,  1, 0, cl};

// line entities
Line(1)   = {1, 2};
Circle(2) = {2, 3, 6};  // start, center, end
Circle(3) = {6, 3, 4};
Line(4)   = {4, 5};
Line(5)   = {5, 12};
Line(6)   = {12, 11};
Circle(7) = {11, 10, 7};
Circle(8) = {7, 10, 9};
Line(9)   = {9, 8};
Line(10)   = {8, 1};

// surface
Line Loop(11) = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
Plane Surface(12) = {11};
