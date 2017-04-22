from color import *
import pygame as pg
from traffic_light import *
from track import *
from direction import *
from car import *
from pedestrian import *
from agent import *
import matplotlib.pyplot as plt


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255,255,0)
GOALCOLOR = (18, 236, 229)
STARTCOLOR = (240, 134, 28)
AGENTCOLOR = (255, 255, 102)
GRAY = (128, 128, 128)
VIOLET = (148,0,211)

def setup():
	traffic_lights = [TrafficLight(10, Color.green, 15, 5, 10), TrafficLight(40, Color.red, 10, 5, 15)]
	pedestrians = []
	pedestrians.append(Pedestrian(0.5, Direction.left, 10))
	pedestrians.append(Pedestrian(0.5, Direction.right, 10))
	pedestrians.append(Pedestrian(0.5, Direction.left, 40))
	pedestrians.append(Pedestrian(0.5, Direction.right, 40))
	cars = []
	cars.append(Car(2, 10, Direction.left, 1, False, 50))
	cars.append(Car(1, 10, Direction.left, 3, False, 50))
	cars.append(Car(2, 10, Direction.left, 2, False, 50))
	cars.append(Car(1, 10, Direction.right, 1, False, 50))
	cars.append(Car(2, 10, Direction.right, 2, False, 50))

	#Parked Cars
	cars.append(Car(1, 15, Direction.right, 0, True, 50))
	cars.append(Car(1, 20, Direction.left, 0, True, 50))
	cars.append(Car(2, 35, Direction.right, 0, True, 50))

	agent = Agent(2, 25, Direction.right, 0, 50, True, 1)
	cars.append(agent)
	track = Track(50, cars, traffic_lights, pedestrians, agent)
	return track

def reset(track, module_num):
	traffic_lights = [TrafficLight(10, Color.green, 15, 5, 10), TrafficLight(40, Color.red, 10, 5, 15)]
	pedestrians = []
	pedestrians.append(Pedestrian(0.5, Direction.left, 10))
	pedestrians.append(Pedestrian(0.5, Direction.right, 10))
	pedestrians.append(Pedestrian(0.5, Direction.left, 40))
	pedestrians.append(Pedestrian(0.5, Direction.right, 40))
	cars = []
	cars.append(Car(2, 10, Direction.left, 1, False, 50))
	cars.append(Car(1, 10, Direction.left, 3, False, 50))
	cars.append(Car(2, 10, Direction.left, 2, False, 50))
	cars.append(Car(1, 10, Direction.right, 1, False, 50))
	cars.append(Car(2, 10, Direction.right, 2, False, 50))

	#Parked Cars
	cars.append(Car(1, 15, Direction.right, 0, True, 50))
	cars.append(Car(1, 20, Direction.left, 0, True, 50))
	cars.append(Car(2, 35, Direction.right, 0, True, 50))

	track.agent.lane = 2
	track.agent.dist = 25
	track.agent.direction = Direction.right
	track.agent.speed = 0
	track.agent.track_len = 50
	track.agent.training = track.agent.training
	track.agent.module_num = module_num

	cars.append(track.agent)
	track = Track(50, cars, traffic_lights, pedestrians, track.agent)
	return track

def draw_lanes(screen):
	pg.draw.line(screen, BLACK, (170,0), (170,680), 1)
	pg.draw.line(screen, BLACK, (340,0), (340,680), 1)
	pg.draw.line(screen, BLACK, (510,0), (510,680), 1)

def draw_agent(screen, agent, track):
	lane = agent.lane
	loc = agent.dist
	direction = agent.direction
	x = 0
	if direction == Direction.right:
		x += 340
	if lane == 2:
		x += 170
	x+= 50
	y = (680 * loc)/track.length
	#rect takes in x,y,width,height
	pg.draw.rect(screen, AGENTCOLOR, (x, y, 50, 680/track.length))	

def draw_lights(screen, traffic_lights, track):
	for light in traffic_lights:
		loc = light.loc
		if light.color == Color.green:
			color = GREEN
		elif light.color == Color.red:
			color = RED
		else:
			color = YELLOW
		y = (680 * loc)/track.length
		pg.draw.rect(screen, color, (0, y, 680, 680/track.length))

def draw_cars(screen, cars, track):
	for car in cars:
		lane = car.lane
		loc = car.dist
		direction = car.direction
		x = 0
		if direction == Direction.right:
			x += 340
		if lane == 2:
			x += 170
		x+= 50
		y = (680 * loc)/track.length
		#rect takes in x,y,width,height
		pg.draw.rect(screen, BLUE, (x, y, 50, 680/track.length))

def draw_pedestrians(screen, pedestrians, track):
	for person in pedestrians:
		lane = person.lane
		loc = person.location
		x = 0
		if not (lane == 0 or lane == 3):
			if person.side == Direction.left:
				if lane == 2:
					x += 170
			else:
				x += 340
				if lane == 2:
					x += 170
			x += 85
			y = (680 * loc)/track.length + 7
			pg.draw.circle(screen, VIOLET, (x,y), 5)


def main():
		track = setup()
		cars = track.cars
		agent = track.agent
		pedestrians = track.pedestrians
		traffic_lights = track.traffic_lights
		state = None
		action = None
		reward = None
		reward_lists = []
		for module_num in range(1,5):
			print "Training Module " + str(module_num)
			track.agent.module_num = module_num
			rewards = []
			for i in range(500):
				print "EPISODE " + str(i + 1)

				pg.init()
				screen = pg.display.set_mode((680, 680))
				pg.display.set_caption("Traffic Simulator")

				track_len = 100
				done = False
				lane_width = 680/4

				clock = pg.time.Clock()
				screen.fill(GRAY)
				pg.display.flip()

				total_reward = 0.0
				for j in range(300):
					for event in pg.event.get():
						if event.type == pg.QUIT:
							done = True
					screen.fill(GRAY)
				 
				 	next_state, next_action, next_reward, done = track.step()
				 	total_reward += (0.9 * next_reward)
				 	if done:
				 		track = reset(track, module_num)
				 		state, action, reward = None, None, None
					if not (state is None or action is None or reward is None):
						track.agent.sarsa(state, action, reward, next_state, next_action, False)
				 	state = next_state
				 	action = next_action
				 	reward = next_reward

					draw_lanes(screen)
					draw_lights(screen, track.traffic_lights, track)
					draw_cars(screen, track.cars, track)
					draw_pedestrians(screen, track.pedestrians, track)
					draw_agent(screen, track.agent, track)
					delay = 0
					pg.display.flip()
					clock.tick(60)
					pg.time.delay(delay)

				track = reset(track, module_num)
				state, action, reward = None, None, None
				rewards.append(total_reward)
			# plt.plot(range(500), rewards)
			# plt.ylabel('Episode Discounted Return')
			# plt.xlabel('Episode Number')
			# if module_num == 1:
			# 	title = "Forward"
			# elif module_num == 2:
			# 	title = "Traffic Light"
			# elif module_num == 3:
			# 	title = "Crash Avoidance"
			# else:
			# 	title= "Pedestrian Avoidance"
			# plt.title(str(title) + " Module")
			# plt.show()
			reward_lists.append(rewards)

		track.agent.training = False
		track.agent.gmq = True
		total_reward = 0
		for j in range(300):
		 	next_state, next_action, next_reward, done = track.step()
		 	total_reward += next_reward
		print "TOTAL REWARD IS " + str(total_reward)

		total_reward = 0
		track.agent.gmq = False
		for j in range(300):
		 	next_state, next_action, next_reward, done = track.step()
		 	total_reward += next_reward
		print "TOTAL REWARD IS " + str(total_reward)

if __name__ == '__main__':
	main()