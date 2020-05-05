#!/usr/bin/python3

import sys
import numpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers

def solve(o1, o2, o3):
	c = matrix([-0.006, -0.004, #b1=x0, c1=x1
	-0.003, -0.009,             #a2=x2, b2=x3
	-0.002, -0.005], tc='d')    #a3=x4, c3=x5	  
	G = matrix([[600, 480, 0, 0, 0, 0],
	[0, 0, 660, 300, 0, 0], 
	[0, 0, 0, 0, 1140, 720], 
	[-1, 0, 0, 0, 0, 0], #b1
	[0, -1, 0, 0, 0, 0], #c1
	[0, 0, -1, 0, 0, 0], #a2
	[0, 0, 0, -1, 0, 0], #b2
	[0, 0, 0, 0, -1, 0], #a3
	[0, 0, 0, 0, 0, -1]  #c3
	], tc='d')
	h = matrix([o1, o2, o3, 0, 0, 0, 0, 0, 0], tc='d')
	A = matrix([[1, -1, 0, 1, 0, -1], 
	[1, 0, -1, 1, -1, 0]], tc='d')
	b = matrix([0, 0], tc='d')
	solution = solvers.lp(c, G.T, h, A.T, b, solver='glpk', options={'glpk':{'msg_lev':'GLP_MSG_OFF'}})
	return (solution['status'] == 'optimal', -solution['primal objective'], solution['x'], solution)

#####################################################################################

def plot(floor, ceiling, type):
	x0 = [] 
	x1 = [] 
	x2 = []
	x3 = []
	x4 = []
	x5 = []
	summ = []
	for x in range(floor, ceiling, 50):
		if type == 1:
			sol = solve(x, 66000, 72600)[2]
		elif type == 2:
			sol = solve(90000, x, 72600)[2]
		elif type == 3:
			sol = solve(90000, 66000, x)[2]
		else:
			print('Неверный тип оборудования!')
			return
		x0.append(sol[0])
		x1.append(sol[1])
		x2.append(sol[2])
		x3.append(sol[3])
		x4.append(sol[4])
		x5.append(sol[5])
		summ.append(sol[0] + sol[3])

	df = pd.DataFrame({'x': range(floor, ceiling, 50),
	                       'B1': x0,
	                       'C1': x1,
	                       'A2': x2,
	                       'B2': x3,
	                       'A3': x4,
	                       'C3': x5, 
	                       'Общее количество изделий A, B, C': summ
	                       })
	plt.plot( 'x', 'Общее количество изделий A, B, C', data=df, color='#003f5c', linewidth=3)
	plt.plot( 'x', 'B1', data=df, marker='', color='#374c80', linewidth=2)
	plt.plot( 'x', 'C1', data=df, marker='', color='#7a5195', linewidth=2)
	plt.plot( 'x', 'A2', data=df, marker='', color='#bc5090', linewidth=2)
	plt.plot( 'x', 'B2', data=df, marker='', color='#ef5675', linewidth=2)
	plt.plot( 'x', 'A3', data=df, marker='', color='#ff764a', linewidth=2)
	plt.plot( 'x', 'C3', data=df, marker='', color='#ffa600', linewidth=2)
	plt.legend()
	plt.xlabel('Фонд времени (мин.)')
	plt.ylabel('Количество изделий (шт.)')
	plt.show()

#####################################################################################

solution = solve(90000, 66000, 72600)

print('Status:', solution[0])
print('Objective:', solution[1])
print('x = \n', solution[2])
x = solution[2]

loaded = []

if (600 * x[0] + 480 * x[1] == 90000) or (660 * x[2] + 300 * x[3] == 66000) or (1140 * x[4] + 720 * x[5] == 72600):
	if 600 * x[0] + 480 * x[1] == 90000:
		loaded.append(1)
	if 660 * x[2] + 300 * x[3] == 66000:
		loaded.append(2)
	if 1140 * x[4] + 720 * x[5] == 72600:
		loaded.append(3)
	print('НОМЕРА ПОЛНОСТЬЮ ЗАГРУЖЕННЫХ ГРУПП: ', loaded)

if 1 in loaded:
	plot(60000, 120000, 1)

if 2 in loaded:
	plot(36000, 96000, 2)

if 3 in loaded:
	plot(42600, 102600, 3)