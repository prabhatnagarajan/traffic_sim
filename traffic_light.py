from color import *
class TrafficLight:
	def __init__(self, loc, lhs_color, rhs_color, green_time, yellow_time, red_time):
		self.lhs_color = lhs_color
		self.rhs_color = rhs_color
		self.green_time = green_time
		self.yellow_time = yellow_time
		self.red_time = red_time