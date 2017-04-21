from direction import *
import random
class Pedestrian:
	def __init__(self, spawn_prob, side, location, lane):
		self.is_spawned = False
		self.spawn_prob = spawn_prob
		self.side = side
		if self.side == Direction.left:
			self.direction = Direction.right
		else:
			self.direction = Direction.left
		self.location = location
		self.lane = lane

	def step(self, track):
		if self.is_spawned:
			if self.direction == Direction.right:
				if self.side == Direction.right:
					if self.lane == 1:
						self.lane = 2
					else:
						self.lane = 3
						self.direction = Direction.left
						self.is_spawned = False
				else:
					if self.lane == 0:
						self.lane = 1
					elif self.lane == 1:
						self.lane = 2
					else:
						self.lane = 1
						self.side = Direction.right 
			else:
				print "Damn"
		else:
			if random.random() < self.spawn_prob:
				is_spawned = True






