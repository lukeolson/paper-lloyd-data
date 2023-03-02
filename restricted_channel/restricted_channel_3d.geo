wallcl = 0.50;

a = 2.82;
p2 = 8;
p1 = 6;
radlo = 1.0;
radhi = 4;

Point(1) = {0, radhi, -p2, wallcl};
Point(2) = {0, radhi, -p1, wallcl};
Point(3) = {0, radlo,   0, wallcl/2};
Point(4) = {0, radhi,  p1, wallcl};
Point(5) = {0, radhi,  p2, wallcl};
Line(1) = {1,2};
Spline(2) = {2,3,4};
Line(3) = {4,5};

out[] = Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} { Line{1,2,3}; };
l1a = out[0]; l2a = out[4]; l3a = out[8];
lcstarta = out[3];
lcenda = out[10];
s1a = out[1]; s2a = out[5]; s3a = out[9];

out[] = Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} { Line{l1a,l2a,l3a}; };
l1b = out[0]; l2b = out[4]; l3b = out[8];
lcstartb = out[3];
lcendb = out[10];
s1b = out[1]; s2b = out[5]; s3b = out[9];

out[] = Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} { Line{l1b,l2b,l3b}; };
l1c = out[0]; l2c = out[4]; l3c = out[8];
lcstartc = out[3];
lcendc = out[10];
s1c = out[1]; s2c = out[5]; s3c = out[9];

out[] = Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} { Line{l1c,l2c,l3c}; };
l1d = out[0]; l2d = out[4]; l3d = out[8];
lcstartd = out[3];
lcendd = out[10];
s1d = out[1]; s2d = out[5]; s3d = out[9];

//For i In {0:11}
//  Printf("out[%g] = %g", i, out[i]);
//EndFor

Line Loop (1001) = {lcstarta,lcstartb,lcstartc,lcstartd};
Line Loop (1002) = {lcenda,lcendb,lcendc,lcendd};

Plane Surface(101) = {1001};
Plane Surface(102) = {1002};
Physical Surface(103) = {101};
Physical Surface(104) = {102};
Physical Surface(105) = {s1a,s2a,s3a,s1b,s2b,s3b,s1c,s2c,s3c,s1d,s2d,s3d};
Surface Loop(106) = {s1a,s2a,s3a,s1b,s2b,s3b,s1c,s2c,s3c,s1d,s2d,s3d,101,102};
Volume(107) = {106};
Physical Volume(1) = {107};

//Volume (1) = {s1a,s2a,s3a,s1b,s2b,s3b,s1c,s2c,s3c,s1d,s2d,s3d,1001,1002};
//Volume (1) = {s1a,s2a,s3a,s1b,s2b,s3b,s1c,s2c,s3c,s1d,s2d,s3d,1001,1002};
//Physical Volume("full") = {1};
