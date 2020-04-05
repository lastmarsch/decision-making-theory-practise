#!/usr/bin/python3

import sys
import numpy as np
import math

class Task1_solver:
	b1 = 0
	b2 = 0
	counter = 3
	optimum_y = 0
	optimum_allocation = []
	results = []

	# initialization
	def __init__(self, funds):
		self.f = funds

	# 1 month function for N1
	def n1(self, x):
		return(4 + (x + 18)**(1/3))

	# 1 month function for N2
	def n2(self, x):
		return(3 + (x + 12)**(1/3)) 

	# balance in N1 at the end of the month
	def n1_balance(self):
		self.b1 = 0.82 * self.b1
		return(self.b1)

	# balance in N2 at the end of the month
	def n2_balance(self):
		self.b2 = 0.92 * self.b2
		return(self.b2)

	# defines the new value of funds needed for reallocation
	def new_funds(self):
		self.f = math.floor(Task1_solver.n1_balance(self) + Task1_solver.n2_balance(self))


	def find_y(self):
		y = 0
		y += self.optimum_y + self.n1(self.b1) + self.n2(self.b2)
		self.results.append(y)
		

	def solve(self):
		for i in range(self.f):
			self.b1 = i
			self.b2 = self.f - i
			Task1_solver.find_y(self)

		self.optimum_y = max(self.results)

		#find optimum b1 and b2 by index of optimum_y
		self.b1 = np.argmax(self.results)
		self.b2 = self.f - np.argmax(self.results)
		self.optimum_allocation.append(self.b1)
		self.optimum_allocation.append(self.b2)

		self.results = []
		self.counter -= 1

		if (self.counter == 0):
			print("----------------RESULT-----------------")
			print("Optimum value of Y: ", self.optimum_y)
			print("Optimum reallocation of funds (X): ")
			print("\t\t N1\t\t N2")
			for i in range(3):
				print("Iteration #", i, "\t", self.optimum_allocation[i * 2], "\t\t", self.optimum_allocation[i* 2 +1])
			print("---------------------------------------")
			return	
		print("Iteration #", -1 * (self.counter - 2))
		print("Optimum value of Y: ", self.optimum_y)
		print()		

		Task1_solver.new_funds(self)
		Task1_solver.solve(self)


def main():
	t = Task1_solver(115)
	Task1_solver.solve(t)

main()


