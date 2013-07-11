Point(1) = {0,0,0};
Point(9) = {0,1,0};
Point(10) = {1,1,0};
Point(11) = {1,0,0};
Point(2) = {0,0.5,0};
Point(3) = {0,0.51,0};
Point(4) = {0,0.511,0};
Point(5) = {0,0.512,0};
Point(6) = {0,0.513,0};
Point(7) = {0,0.514,0};
Point(8) = {0,0.515,0};


Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,11};
Line(11) = {11,1};

Compound Line(15) = {1,2,3,4,5,6,7,8,9};
Compound Line(16) = {10,11};
//Compound Surface(1) = {1,2};

//Physical Line(6) = {15};
//Physical Line(5) = {16};

Line Loop(1) = {1,2,3,4,5,6,7,8,9,10,11};
Plane Surface(1) = {1};
Compound Surface(2) = {1};

Field[1] = MathEval;
Field[1].F = "0.1";
Background Field = 1;
