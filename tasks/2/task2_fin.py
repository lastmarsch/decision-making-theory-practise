#!/usr/bin/python3

import sys
import numpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers

def solve(o1, o2, o3):
	c = matrix([0, -0.006, -0.004, #b1, c1
	-0.003, -0.009, 0,  #a2, b2
	-0.002, 0, -0.005], tc='d') #a3, c3	  
	G = matrix([[0, 10, 8, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 11, 5, 0, 0, 0, 0], 
	[0, 0, 0, 0, 0, 0, 19, 0, 12], 
	# [-1, 0, 0, 0, 0, 0, 0, 0, 0], #a1
	[0, -1, 0, 0, 0, 0, 0, 0, 0], #b1
	[0, 0, -1, 0, 0, 0, 0, 0, 0], #c1
	[0, 0, 0, -1, 0, 0, 0, 0, 0], #a2
	[0, 0, 0, 0, -1, 0, 0, 0, 0], #b2
	# [0, 0, 0, 0, 0, -1, 0, 0, 0], #c2
	[0, 0, 0, 0, 0, 0, -1, 0, 0], #a3
	# [0, 0, 0, 0, 0, 0, 0, -1, 0], #b3
	[0, 0, 0, 0, 0, 0, 0, 0, -1]  #c3
	], tc='d')
	h = matrix([o1, o2, o3, 0, 0, 0, 0, 0, 0], tc='d')
	A = matrix([[1, -1, 0, 1, -1, 0, 1, -1, 0], 
	[0, 1, -1, 0, 1, -1, 0, 1, -1], 
	[-1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, -1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, -1, 0]], tc='d')
	b = matrix([0, 0, 0, 0, 0], tc='d')
	solution = solvers.lp(c, G.T, h, A.T, b, solver='glpk', options={'glpk':{'msg_lev':'GLP_MSG_OFF'}})
	return (solution['status'] == 'optimal', -solution['primal objective'], solution['x'], solution)

#####################################################################################

def plot(title, floor, ceiling, direction):
	x0 = [] 
	x1 = [] 
	x2 = []
	x3 = []
	x4 = []
	x5 = []
	x6 = [] 
	x7 = [] 
	x8 = []
	for x in range(floor, ceiling):
		sol = solve(x, 1100, 1210)[2]
		x0.append(sol[0])
		x1.append(sol[1])
		x2.append(sol[2])
		x3.append(sol[3])
		x4.append(sol[4])
		x5.append(sol[5])
		x6.append(sol[6])
		x7.append(sol[7])
		x8.append(sol[8])

	df = pd.DataFrame({'x': range(floor, ceiling),
	                       'A1': x0,
	                       'B1': x1,
	                       'C1': x2,
	                       'A2': x3,
	                       'B2': x4,
	                       'C2': x5,
	                       'A3': x6,
	                       'B3': x7,
	                       'C3': x8})
	plt.plot( 'x', 'A1', data=df, marker='', color='#808080', linewidth=2)
	plt.plot( 'x', 'B1', data=df, marker='', color='green', linewidth=2)
	plt.plot( 'x', 'C1', data=df, marker='', color='red', linewidth=2)
	plt.plot( 'x', 'A2', data=df, marker='', color='magenta', linewidth=2)
	plt.plot( 'x', 'B2', data=df, marker='', color='blue', linewidth=2)
	plt.plot( 'x', 'C2', data=df, marker='', color='#8a7f8e', linewidth=2)
	plt.plot( 'x', 'A3', data=df, marker='', color='yellow', linewidth=2)
	plt.plot( 'x', 'B3', data=df, marker='', color='#997a8d', linewidth=2)
	plt.plot( 'x', 'C3', data=df, marker='', color='cyan', linewidth=2)
	plt.legend()
	plt.xlabel('Фонд времени')
	plt.ylabel('Количество изделий')
	plt.title(title)
	if direction == -1:
		plt.gca().invert_xaxis()
	plt.show()

#####################################################################################

solution = solve(1500, 1100, 1210)

print('Status:', solution[0])
print('Objective:', solution[1])
print('x = \n', solution[2])
x = solution[2]

loaded = []

if (10 * x[1] + 8 * x[2] == 1500) or (11 * x[3] + 5 * x[4] == 1100) or (19 * x[6] + 12 * x[8] == 1210):
	if 10 * x[1] + 8 * x[2] == 1500:
		loaded.append(1)
	if 11 * x[3] + 5 * x[4] == 1100:
		loaded.append(2)
	if 19 * x[6] + 12 * x[8] == 1210:
		loaded.append(3)
	print('НОМЕРА ПОЛНОСТЬЮ ЗАГРУЖЕННЫХ ГРУПП: ', loaded)

if 1 in loaded:
	plot('Увеличение фонда 1', 1500, 2000, 1)
	plot('Уменьшение фонда 1', 1000, 1500, -1)

if 2 in loaded:
	plot('Увеличение фонда 2', 1100, 1600, 1)
	plot('Уменьшение фонда 2', 600, 1100, -1)

if 3 in loaded:
	plot('Увеличение фонда 3', 1210, 1910, 1)
	plot('Уменьшение фонда 3', 710, 1210, -1)
