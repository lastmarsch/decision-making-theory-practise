#!/usr/bin/python3

import sys
import numpy
from cvxopt import matrix, solvers

# initialization
Y = matrix([0, -0.006, -0.004, #b1, c1
	-0.003, -0.009, 0,  #a2, b2
	-0.002, 0, -0.005], tc='d') #a3, c3
# print('c:')
# print(Y)

T = matrix([[0, 10, 8, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 11, 5, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 19, 0, 12], 
	[-1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, -1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, -1, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, -1, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, -1, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, -1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, -1, 0, 0], 
	[0, 0, 0, 0, 0, 0, 0, -1, 0], 
	[0, 0, 0, 0, 0, 0, 0, 0, -1]], tc='d')
# print('G:')
# print(T)

time_funds = matrix([1500, 1100, 1210, 
	0, 0, 0, 0, 0, 0, 0, 0, 0], tc='d')
# print('h:')
# print(time_funds)
# print()

A = matrix([[1, 1, 1, -1, -1, -1, 0, 0, 0], 
	[0, 0, 0, 1, 1, 1, -1, -1, -1]], tc='d')
# print('A:')
# print(A)
# print()

b = matrix([0, 0], tc='d')
# print('b:')
# print(b)
# print()

#solve
solution = solvers.lp(Y, T.T, time_funds, A.T, b, solver='glpk')
print()
print('Status:', solution['status'])
print('Objective:', -solution['primal objective'])
print('x =', solution['x'])
print()

x = solution['x']

if (10 * x[1] + 8 * x[2] == 1500) or (11 * x[3] + 5 * x[4] == 1100) or (19 * x[6] + 12 * x[8] == 1210):
	print('В РЕШЕНИИ ПРИСУТСТВУЕТ ПОЛНОСТЬЮ ЗАГРУЖЕННАЯ ГРУППА ОБОРУДОВАНИЯ\n')

dh = matrix([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
solution1 = solvers.lp(Y, T.T, time_funds+dh, A.T, b, solver='glpk')
print()
print('Status:', solution1['status'])
print('Objective:', -solution1['primal objective'],
	'delta:', -solution1['primal objective']-(-solution['primal objective']))
print('x =', solution1['x'])
print()


print('УВЕЛИЧЕНИЕ ФОНДА РАБОЧЕГО ВРЕМЕНИ')
prev_z = -solution['primal objective']
a = 1
while (True):
	solution_i = solvers.lp(Y, T.T, time_funds + dh * a, A.T, b, solver='glpk')
	if solution_i['status'] != 'optimal':
		print('Couldn''t find a solution!')
		break
	new_z = -solution_i['primal objective']
	delta_z = new_z - prev_z
	print('Increment %d: objective = %.4f delta = %.4f' % (a, new_z, delta_z))
	if abs(delta_z - 1500) > 1e-6:
		print('Basis changed at increment %d' % (a,))
		break
	prev_z = new_z
	a += 1

print('\nУМЕНЬШЕНИЕ ФОНДА РАБОЧЕГО ВРЕМЕНИ')
prev_z = -solution['primal objective']
a2 = -1
while (True):
	solution_i = solvers.lp(Y, T.T, time_funds + dh * a2, A.T, b, solver='glpk')
	if solution_i['status'] != 'optimal':
		print('Couldn''t find a solution!')
		break
	new_z = -solution_i['primal objective']
	delta_z = new_z - prev_z
	print('Increment %d: objective = %.4f delta = %.4f' % (a2, new_z, delta_z))
	if abs(delta_z - 1500) > 1e-6:
		print('Basis changed at increment %d' % (a2,))
		break
	prev_z = new_z
	a2 -= 1