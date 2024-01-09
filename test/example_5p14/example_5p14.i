#*PROBLEM_DIM
#1
*NODE
1   0   0   0
2   1   0   0
3   2   0   0
4   2.5   0   0
5   3   0   0
6   3.5 0   0   
7   4   0   0
8   4.5 0   0
9   5   0   0
*ELEMENT
#ID NDS
E1QUD   1   1   3   2
E1QUD   2   3   5   4
E1QUD   3   5   7   6   
E1QUD   4   7   9   8
*BOUNDARY_ESSENTIAL
#TYPE EntityID dofs
ESSENTIAL 1   0
ESSENTIAL 9   0
*BOUNDARY_IMPOSED
Load_Node 7
Load_Element 1
