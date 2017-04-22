import numpy as np
import random
from color import *
from pdb import set_trace

class Agent:
	def __init__(self, lane, dist, direction, speed, track_len, training, module_num):
		self.lane = lane
		self.dist = dist
		self.direction = direction
		self.speed = speed
		self.track_len = track_len
		#module is 0 to 3
		self.module_num = module_num
		self.training = training
		#add Q functions
		#consists of (speed, lane) tuples
		self.actions = [(0,1), (0,2), (1,1), (1,2), (2,1), (2,2), (3,1), (3,2)]
		num_actions = len(self.actions)
		self.q_funcs = dict()
		self.q_funcs[1] = np.zeros((50, num_actions))
		# self.q_funcs[2] = np.zeros((len(state_1), num_actions))
		# self.q_funcs[3] = np.zeros((len(state_1), num_actions))
		# self.q_funcs[4] = np.zeros((len(state_1), num_actions))
		self.discounts = dict()
		self.discounts[1] = 0.9
		self.discounts[2] = 0.9
		self.discounts[3] = 0.9
		self.discounts[4] = 0.9
		self.epsilons = dict()
		self.epsilons[1] = 0.075
		self.epsilons[2] = 0.075
		self.epsilons[3] = 0.075
		self.epsilons[4] = 0.075
		self.state_spaces = dict()
		self.state_spaces[1] = range(50)

	def step(self, track):
		if self.training:
			return self.train(track)
		else:
			print "combining all policies"

	def train(self, track):
		discount = self.discounts[self.module_num]
		states = self.state_spaces[self.module_num]
		epsilon = self.epsilons[self.module_num]
		Q = self.q_funcs[self.module_num]
		state = self.get_state(track)
		#epsilon greedy
		if random.random() < epsilon:
			speed, lane = random.choice(self.actions)
		else:
			speed, lane = self.actions[np.argmax(Q[state,:])]
		return self.act(speed, lane, track)

	def act(self, speed, lane, track):
		ran_red = self.is_run_red_light(speed, lane, track)
		car_collision = self.is_car_collision(speed, lane, track)
		if ran_red:	
			print "RAND RED"
		if car_collision:
			print "COLLISION" 
		self.dist = (self.dist - speed + track.length) % track.length
		self.lane = lane
		return True

	def is_car_collision(self, speed, lane, track):
		positions = range((self.dist - speed + track.length) % track.length, self.dist + 1)
		for car in track.cars:
			if isinstance(car, Agent):
				continue
			if car.direction == self.direction:
				if car.dist in positions:
					if car.lane == lane:
						return True
		return False
		
	def is_run_red_light(self, speed, lane, track):
		positions = range((self.dist - speed + track.length) % track.length, self.dist + 1)
		for light in track.traffic_lights:
			if light.color == Color.red:
				if light.loc in positions:
					return True
		return False

	def get_state(self, track):
		if self.module_num == 1:
			return self.dist