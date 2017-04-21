from color import *
import pygame as pg
from traffic_light import *
from track import *
from direction import *
from car import *
from pedestrian import *

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


def draw_lanes(screen):
	pg.draw.line(screen, BLACK, (170,0), (170,680), 1)
	pg.draw.line(screen, BLACK, (340,0), (340,680), 1)
	pg.draw.line(screen, BLACK, (510,0), (510,680), 1)

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
		traffic_lights = [TrafficLight(10, Color.green, 10, 5, 40), TrafficLight(40, Color.red, 10, 5, 35)]
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
		cars.append(Car(2, 15, Direction.right, 0, True, 50))
		cars.append(Car(1, 20, Direction.left, 0, True, 50))
		cars.append(Car(2, 35, Direction.right, 0, True, 50))

		track = Track(50, cars, traffic_lights, pedestrians, None)
		pg.init()
		screen = pg.display.set_mode((680, 680))
		pg.display.set_caption("Traffic Simulator")
		track_len = 100
		#fill with white
		done = False
		lane_width = 680/4
		clock = pg.time.Clock()
		# If you want a background image, replace this clear with blit'ing the
	    # background image.
		screen.fill(GRAY)
	 
	    # --- Drawing code should go here
		pg.display.flip()
		reward = 0.0
		while not done:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					done = True
		 
		    # --- Game logic should go here
		    # --- Screen-clearing code goes here
		 
		    # Here, we clear the screen to white. Don't put other drawing commands
		    # above this, or they will be erased with this command.
		 
		    # If you want a background image, replace this clear with blit'ing the
		    # background image.
			screen.fill(GRAY)
		 
		 	track.step()
		    # --- Drawing code should go here
			draw_lanes(screen)

			draw_lights(screen, track.traffic_lights, track)
			draw_cars(screen, cars, track)
			draw_pedestrians(screen, pedestrians, track)
		    # --- Go ahead and update the screen with what we've drawn.
			delay = 250
			# if agent.get_loc() == self.goal:
			# 	delay = 680
			# 	done = True
			pg.display.flip()
		    # --- Limit to 60 frames per second
			clock.tick(60)
			pg.time.delay(delay)
			# wait

if __name__ == '__main__':
	main()