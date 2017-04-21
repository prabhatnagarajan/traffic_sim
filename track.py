from agent import *
class Track:
	def __init__(self, length, cars, traffic_lights, pedestrians, agent):
		self.length = length
		self.cars = cars
		self.traffic_lights = traffic_lights
		self.pedestrians = pedestrians
		self.agent = agent

	def step(self):
		for car in self.cars:
			if not isinstance(car, Agent):
				car.step(self)
		for light in self.traffic_lights:
			light.step()
		for person in self.pedestrians:
			person.step(self)
		return self.agent.step(self)

