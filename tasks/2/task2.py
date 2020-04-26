#!/usr/bin/python3

import sys
import numpy
from cvxopt import matrix
from cvxopt.modeling import variable, op

# initialization
Y = [0.006, 0.004, #b1, c1
	0.003, 0.009,  #a2, b2
	0.002, 0.005] #a3, c3
print('Product Y consumption:')
print(Y)

T = [10, 8,
	11, 5,
	19, 12]
print('Time parameters:')
print(T)

time_funds = [1500, 1100, 1210]
print('Time funds:')
print(time_funds)
print()

# variables
x = variable(6, 'x')

# function
f = - (Y[0] * x[0] + Y[1] * x[1] + Y[2] * x[2] +
	Y[3] * x[3] + Y[4] * x[4] + Y[5] * x[5])

o1 = (T[0] * x[0] + T[1] * x[1] <= time_funds[0])
o2 = (T[3] * x[3] + T[2] * x[2] <= time_funds[1])
o3 = (T[4] * x[4] + T[5] * x[5] <= time_funds[2])
o4 = (x[2] + x[4] == x[0] + x[3]) # A = B
o5 = (x[0] + x[3] == x[1] + x[5]) # B = C
x_non_negative = (x >= 0)    
problem = op (f, [o1, o2, o3, o4, o5, x_non_negative])
problem.solve(solver = 'glpk')  
problem.status
print ("Прибыль:")
print(abs(problem.objective.value()[0]))
print ("Результат:")

res = x.value
for i in range(len(res)):
	print('x[', i, '] = ', res[i])

print(res[2] + res[4])
print(res[1] + res[5])
print(res[0] + res[3])


