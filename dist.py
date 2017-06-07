#!/usr/bin/python

from Tkinter import *
import ttk
import matplotlib.pyplot as plt
import numpy as np


class Application(Frame):
	def strt(self):
		self.sr=float(self.text1.get())
		self.lr=float(self.text2.get())
		self.hn=float(self.text3.get())

		self.dx=float(self.sr)/self.hn
		self.rinit=0
		self.pi=3.14

		self.rs=[ i*self.dx for i in range(self.hn) ]
		self.ans=[ self.pi*i*self.dx for i in range(self.hn) ]
		self.y_pos= np.arange(len(self.rs))

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
		self.text1.set('Small Radius')
		self.a1 = Entry(textvariable=self.text1)
		self.a1.pack()

		self.text2 = StringVar()
		self.text2.set('Large Radius')
		self.a2 = Entry(textvariable=self.text2)
		self.a2.pack()

		self.text3 = StringVar()
		self.text3.set('Hist Parts')
		self.a3 = Entry(textvariable=self.text3)
		self.a3.pack()

		print(self.text3.get())


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

