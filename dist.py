#!/usr/bin/python

from Tkinter import *
import ttk
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import math


class Application(Frame):

	# counts integral for sqrt(x^2 - x^2) for the given x (^2 being square)
	def count_integral(self,c, x):
		return c * ((c * math.asin(x / c)) + (x * math.sqrt((c * c) - (x * x)) / math.fabs(c))) / 2.0


	# counts integral for sqrt(x^2 - x^2) for the given range (x0 to x1) (^2 being square)
	def count_definite_integral(self,c, x0, x1):
		return self.count_integral(c, x1) - self.count_integral(c, x0)


	# counts the possibility, that the dot lies within the radius range (0 to r)
	# inside an ellipse with small radius a and big radius b
	def count_probability(self,a, b, r):
		if a > b:
			tmp = a
			a = b
			b = tmp
		if r <= a:
			return (r * r) / (a * b)
		if r >= b:
			return 1.0
		k = math.sqrt(((a * a) - (r * r)) / (((a * a) / (b * b)) - 1))
		ellipse_quarter = (a * self.count_definite_integral(b, 0, k) / b)
		circle_quarter = self.count_definite_integral(r, k, r)
		s = 4.0 * (ellipse_quarter + circle_quarter)
		return s / (a * b * math.pi)


	# counts the possibility, that the dot lies within the radius range (r0 to r1)
	# inside an ellipse with small radius a and big radius b
	def count_probability_range(self,a, b, r0, r1):
		return math.fabs(self.count_probability(a, b, r0) - self.count_probability(a, b, r1))


	# create csv file containing probability from each radius to radius + dx, 
	# where dx is small change of radius
	def make_csv(self,rs,rr,ans):
		with open('names.csv', 'w') as csvfile:
			fieldnames = ['r0', 'r1', 's']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()

			for x in range(self.hn):
				writer.writerow({'r0': self.rs[x], 'r1': self.rr[x], 's': self.ans[x]})


	def strt(self):
		self.sr=float(self.text1.get())
		self.lr=float(self.text2.get())
		self.hn=int(self.text3.get())

		self.dx=float(self.lr)/self.hn
		self.rinit=0
		self.pi=3.14

		self.rs=[ i*self.dx for i in range(self.hn) ]
		self.rr=[ (1+i)*self.dx for i in range(self.hn) ]
		self.ans=[ self.count_probability_range(self.sr,self.lr,i*self.dx,(i+1)*self.dx) for i in range(self.hn) ]
		self.y_pos= np.arange(self.hn)

		self.make_csv(self.rs,self.rr,self.ans)
		
		plt.bar(self.y_pos, self.ans, align='center')
		plt.xticks(self.y_pos,self.rs)
		plt.ylabel('ans')

		plt.show()


	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit

		self.QUIT.pack({"side": "left"})

		self.START = Button(self)
		self.START["text"] = "Start",
		self.START["command"] = self.strt

		self.START.pack({"side": "left"})
		
		self.text1 = StringVar()
		self.text1.set('small radius')
		self.a1 = Entry(textvariable=self.text1)
		self.a1.pack()

		self.text2 = StringVar()
		self.text2.set('large radius')
		self.a2 = Entry(textvariable=self.text2)
		self.a2.pack()

		self.text3 = StringVar()
		self.text3.set('num of parts')
		self.a3 = Entry(textvariable=self.text3)
		self.a3.pack()


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
