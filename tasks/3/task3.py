#!/usr/bin/python3

import sys
import numpy
from cvxopt import matrix, solvers
from math import floor
from prettytable import PrettyTable

	
def solve(index, type, iter):

	line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	if type == 'plus':
		line[index] = iter * 0.1
	if type == 'minus':
		line[index] = iter * -0.1

	dc = matrix(line, tc='d')

	c = matrix([
		[7.3, 6.1, 7.4, 7.5, 3.6,
		6.9, 4.2, 4.2, 5.2, 6.6,
		6.0, 7.1, 7.5, 7.0, 7.8, 
		4.2, 5.0, 7.8, 2.7, 2.6,
		0, 0, 0, 0, 0]
		], tc='d')

	G = matrix([
		[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
		[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
		], tc='d')

	#a1 = 381
	h = matrix([
		381, 4100, 5300, 5600, 5964,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
		], tc='d')

	A = matrix([
		[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
		], tc='d')

	# 0.62 * (381 + 4100 + 5300 + 5600) = 9536
	b = matrix([
		3000, 2700, 2400, 3200, 4200, 9536
		], tc='d')

	solution = solvers.lp(c + dc, G.T, h, A.T, b, solver='glpk', options={'glpk':{'msg_lev':'GLP_MSG_OFF'}})
	return (solution['status'] == 'optimal', solution['primal objective'], solution['x'], solution)

def plus_included(solution):
	included = []
	if solution[0] != 0:
		included.append(0)
	if solution[5] != 0:
		included.append(5)
	if solution[8] != 0:
		included.append(8)
	if solution[11] != 0:
		included.append(11)
	if solution[16] != 0:
		included.append(16)
	print('\nИндексы цен с + (входящих в решение):', included)
	return(included)

def minus_not_included(solution):
	included = []
	if solution[7] == 0:
		included.append(7)
	if solution[9] == 0:
		included.append(9)
	if solution[13] == 0:
		included.append(13)
	print('Индексы цен с - (не входящих в решение):', included)
	return(included)

print('A1 = 381')
total = floor(0.62 * (381 + 4100 + 5300 + 5600))
need = 3000 + 2700 + 2400 + 3200 + 4200
print('Запасы:', total)
print('Требуется:', need)
if need < total:
	print("Избыток: %.2f" % (need/total * 100),"%")
else: print("Недостаток: %.2f" % (total/need * 100),"%")
print('Ввод фиктивного поставщика А5 =', need-total)

# решение
print('\nРешение:')
solution = solve(0, 0, 0)
# print('Status:', solution[0])
print("Значение ЦФ: %.2f" % (solution[1]))
# print('x = ', solution[2])
original_value = solution[1]

x = solution[2]
cols = 5
table = PrettyTable(['B1', 'B2', 'B3', 'B4', 'B5'])
td = x[:]
while td:
    table.add_row(td[:cols])
    td = td[cols:]
print(table)

plus = plus_included(x)
minus = minus_not_included(x)

changed_value_plus = []
for index in plus:
	iter = 1
	sol = solve(index, 'plus', iter)
	while sol[2][index] != 0:
		iter += 1
		sol = solve(index, 'plus', iter)
	changed_value_plus.append((index, sol[1]))

changed_value_minus = []
for index in minus:
	iter = 1
	sol = solve(index, 'minus', iter)
	while sol[2][index] == 0:
		iter += 1
		sol = solve(index, 'minus', iter)
	changed_value_minus.append((index, sol[1]))

print('\nПроверка на чувствительность к изменению ЦФ:')
print("\nИзначальное значение ЦФ: %.2f" % (original_value))
if changed_value_plus != []:
	print('\nЦены с тенденцией к увеличению:\nИндекс\tЗначение ЦФ\tРазница')
for item in changed_value_plus:
	print(item[0], "\t%.2f" % (item[1]), "\t%.2f" % (item[1]-original_value))
if changed_value_minus != []:
	print('\nЦены с тенденцией к уменьшению:\nИндекс\tЗначение ЦФ\tРазница')
for item in changed_value_minus:
	print(item[0], "\t%.2f" % (item[1]), "\t%.2f" % (item[1]-original_value))