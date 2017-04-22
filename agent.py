import numpy as np
import random
from color import *
from direction import *
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
		self.q_funcs[2] = np.zeros((50 * 3 * 3, num_actions))
		self.q_funcs[3] = np.zeros((50 * 2, num_actions))
		self.q_funcs[4] = np.zeros((800, num_actions))
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
		self.state_spaces[2] = range(50 * 3 * 3)
		self.state_spaces[3] = range(50 * 2)
		self.state_spaces[4] = range(800)
		self.gmq = False
		self.topq = False

	def step(self, track):
		if self.training:
			return self.train(track)
		else:
			return self.test(track)

	def train(self, track):
		states = self.state_spaces[self.module_num]
		epsilon = self.epsilons[self.module_num]
		Q = self.q_funcs[self.module_num]
		state = self.get_state(track)
		#epsilon greedy
		action = self.choose_action(epsilon, Q, state)
		speed, lane =self.actions[action]
		reward, done = self.act(speed, lane, track)
		return (state, action, reward, done)

	def test(self, track):
		if self.gmq:
			sum_val = 0.0
			qs = []
			for action in self.actions:
				for module in (1,5):
					states = self.state_spaces[module]
					Q = self.q_funcs[module]
					self.module_num = module
					state = self.get_state(track)
					sum_val += Q[state, action]
			qs.append(sum_val)
			best_action = qs.index(max(qs))
			speed, lane =self.actions[best_action]
			reward, done = self.act(speed, lane, track)
			return (state, action, reward, done)
		else:
			maxq = -10000
			best_action = 0
			for action in self.actions:
				for module in (1,5):
					states = self.state_spaces[module]
					Q = self.q_funcs[module]
					self.module_num = module
					state = self.get_state(track)
					if Q[state, action] > maxq:
						maxq = Q[state, action]
						best_action = action
			speed, lane = self.actions[best_action]
			reward, done = self.act(speed, lane, track)
			return (state, action, reward, done)

	def sarsa(self, state, action, reward, next_state, next_action, done):
		discount = self.discounts[self.module_num]
		Q = self.q_funcs[self.module_num]
		if not done:
			self.q_funcs[self.module_num][state, action] = Q[state, action] + 0.1 * (reward + discount * Q[next_state, next_action] - Q[state, action])
		else:
			self.q_funcs[self.module_num][state, action] = Q[state, action] + 0.1 * (reward + discount * 0 - Q[state, action])

	def choose_action(self, epsilon, Q, state):
		if random.random() < epsilon:
			return random.randint(0, len(self.actions) - 1)
		else:
			return np.argmax(Q[state,:])

	def act(self, speed, lane, track):
		ran_red = self.is_run_red_light(speed, lane, track)
		car_collision = self.is_car_collision(speed, lane, track)
		ped_collision = self.pedestrian_collision(speed, lane, track)
		self.dist = (self.dist - speed + track.length) % track.length
		self.lane = lane
		if self.module_num == 1:
			reward = float(speed)
		if self.module_num == 2:
			reward = 0.01
			if ran_red:
				reward = -10.0
		if self.module_num == 3:
			reward = 0.01
			if car_collision:
				reward = -20.0
		if self.module_num == 4:
			reward = 0.01
			if ped_collision:
				reward = -100.0
		return (reward, (ran_red or car_collision or ped_collision))

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

	def pedestrian_collision(self, speed, lane, track):
		positions = range((self.dist - speed + track.length) % track.length, self.dist + 1)
		for person in track.pedestrians:
			if person.side == self.direction:
				if person.location in positions:
					if person.lane == lane:
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
		if self.module_num == 2:
			value = self.dist
			value = value * 9
			val1 = 0
			val2 = 0
			if track.traffic_lights[0] == Color.yellow:
				val1 = 1
			if track.traffic_lights[0] == Color.red:
				val1 = 2
			if track.traffic_lights[1] == Color.yellow:
				val2 = 1
			if track.traffic_lights[1] == Color.red:
				val2 = 2
			value += val1 * 3 
			value += val2
			return value
		if self.module_num == 3:
			return (self.lane - 1) * 50 + self.dist
		if self.module_num == 4:
			ped1 = False
			ped2 = False
			ped3 = False
			ped4 = False
			for person in track.pedestrians:
				if person.side == Direction.right:
					if person.lane == 1:
						if person.location == 10:
							ped1 = True
						if person.location == 40:
							ped2 = True
					if person.lane == 1:
						if person.location == 10:
							ped3 = True
						if person.location == 40:
							ped4 = True
			value = 0
			if ped1:
				value += 400
			if ped2:
				value += 200
			if ped3:
				value += 100
			if ped4:
				value += 50
			value += self.dist
			return value



