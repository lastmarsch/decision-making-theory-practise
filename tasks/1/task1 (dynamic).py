#!/usr/bin/python3

import sys
import numpy as np
import math

class Task1_solver:

	# Словарь со значениями выигрышей на разных этапах
	# Ключ - пара (month, funds) = (stage, state)
	# Значение - пара (profit, x_N1) = (profit, control)
	w_table = {}

	# Инициализация
	def __init__(self, months):
		self.months = months

	# Выручка в N1 в течение одного месяца 
	def c1(self, x):
		return(4 + (x + 18)**(1/3))

	# Выручка в N2 в течение одного месяца
	def c2(self, x):
		return(3 + (x + 12)**(1/3)) 

	# Остаток средств в N1 в конце месяца
	def n1_balance(self, x):
		return(0.82 * x)

	# Остаток средств в N2 в конце месяца
	def n2_balance(self, x):
		return(0.92 * x)

	# Пересчет доступных средств 
	# funds = state (суммарное количество X), x_N1 = control (количество X в N1)
	def transition(self, funds, x_N1):
		return(math.floor(
			self.n1_balance(x_N1) 
			+ self.n2_balance(funds - x_N1)
			))

	# Выигрыш на данном этапе
	# funds = state (суммарное количество X), x_N1 = control (количество X в N1)
	def profit(self, funds, x_N1): 
		return(self.c1(x_N1) + self.c2(funds - x_N1))  
		

	def w(self, month, state):
		if month >= self.months:
			return (0, None)

		if (month, state) in self.w_table:
			return self.w_table[(month, state)]

		best_control = None
		best_profit = None

		for x in range(state):
			control = x	
			control_eval = self.profit(state, control) 
			+ self.w(month + 1, self.transition(state, control))[0]
			if best_profit == None or control_eval > best_profit:
				best_profit = control_eval
				best_control = control

		self.w_table[(month, state)] = (best_profit, best_control)
		return(best_profit, best_control)

	def restore_optimal_control(self, state):
		optimal_control_sequence = []
		for month in range(self.months):
			control = self.w_table[(month, state)][1]
			optimal_control_sequence.append(control)
			state = self.transition(state, control)
		return optimal_control_sequence  

	def answer(self, seq, funds):
		sum_profit = 0
		for i in range(len(seq)):
			print("Month #", i, "\t", 
				  seq[i], "\t\t", 
				  funds - seq[i], "\t\t",
				  self.profit(funds, seq[i]))
			sum_profit += self.profit(funds, seq[i])
		return(sum_profit)


	def solve(self, funds):
		self.w(0, funds)
		print("\t\t N1\t\t N2\t\t Y")
		print("Sum Y = ", self.answer(
				self.restore_optimal_control(funds), 
				funds
				)
			)


def main():
	x = 115
	t = Task1_solver(3)
	t.solve(x)

main()


