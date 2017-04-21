from color import *
from pdb import set_trace
class TrafficLight:
	def __init__(self, loc, color, green_time, yellow_time, red_time):
		self.loc = loc
		self.color = color
		self.green_time = green_time
		self.yellow_time = yellow_time
		self.red_time = red_time
		self.counter = 1

	def step(self):
		self.counter += 1
		if self.color == Color.red:
			if self.counter % self.red_time == 0:
				self.color = Color.green
				self.counter = 1
		if self.color == Color.green:
			if self.counter % self.green_time == 0:
				self.color = Color.yellow
				self.counter = 1
		if self.color == Color.yellow:
			if self.counter % self.yellow_time == 0:
				self.color = Color.red
				self.counter = 1
		return self.color