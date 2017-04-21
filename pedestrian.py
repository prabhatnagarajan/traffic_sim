from direction import *
from color import *
import random
class Pedestrian:
	def __init__(self, spawn_prob, side, location):
		self.is_spawned = False
		self.spawn_prob = spawn_prob
		self.side = side
		if self.side == Direction.left:
			self.direction = Direction.right
		else:
			self.direction = Direction.left
		self.location = location
		if self.side == Direction.left:
			self.lane = 0
		else:
			self.lane = 3

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
				if self.side == Direction.right:
					if self.lane == 3:
						self.lane = 2
					elif self.lane == 2:
						self.lane = 1
					else:
						self.lane = 2
						self.side = Direction.left
				else:
					if self.lane == 2:
						self.lane = 1
					else:
						self.lane = 0
						self.direction = Direction.right
						self.is_spawned = False 
		else:
			red = False
			for signal in track.traffic_lights:
				if signal.loc == self.location:
					if signal.color == Color.red and (signal.red_time - signal.counter) >= 4:
						red = True
						break
			if random.random() < self.spawn_prob:
				if red:
					self.is_spawned = True
				else:
					if random.random() < 0.03:
						self.is_spawned = True








