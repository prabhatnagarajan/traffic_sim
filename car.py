from direction import *
class Car:
	def __init__(self, lane, dist, direction, speed, parked, track_len):
		self.lane = lane
		self.dist = dist
		self.direction = direction
		self.speed = speed
		self.parked = parked

	def step(self, track):
		if self.parked:
			return
		start = self.dist
		if self.direction == Direction.left:
			direction = 1
		else:
			direction = -1
		self.dist = (self.dist + (self.speed * direction) + track.length) % track.length
		# for pedestrian in track.pedestrians:
		# 	collision = self.collision(start, self.dist)

	def collision(self, start, new, location):
		if new > start:
			return location < new or location > start
		else:
			return location > start and location <= new
