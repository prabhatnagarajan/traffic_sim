from direction import *
from color import *

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
		speed = self.speed
		if self.direction == Direction.left:
			direction = 1
		else:
			direction = -1
		signal = self.get_signal_ahead(track)
		if not (signal is None):
			if signal.color == Color.yellow or signal.color == Color.red:
				speed = min(speed, 1)
			if signal.color == Color.red and signal.loc == self.dist + 1:
				speed = 0
		self.dist = (self.dist + (speed * direction) + track.length) % track.length


	def collision(self, start, new, location):
		if new > start:
			return location < new or location > start
		else:
			return location > start and location <= new

	def get_signal_ahead(self, track):
		ahead = []
		for signal in track.traffic_lights:
			if self.direction == Direction.left:
				if self.dist < signal.loc:
					ahead.append(signal) 
			else:
				if self.dist > signal.loc:
					ahead.append(signal)
		if len(ahead) == 0:
			return None
		closest_signal = ahead[0]
		if self.direction == Direction.left:
			for signal in ahead:
				if signal.loc < closest_signal.loc:
					closest_signal = signal
		else:
			for signal in ahead:
				if signal.loc > closest_signal.loc:
					closest_signal = signal
		return closest_signal
