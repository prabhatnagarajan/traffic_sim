from color import *
import pygame as pg
from traffic_light import *
from track import *
from direction import *
from car import *

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


def setup():
	print "Do nothing"

def draw_lanes(screen):
	pg.draw.line(screen, BLACK, (250,0), (250,1000), 1)
	pg.draw.line(screen, BLACK, (500,0), (500,1000), 1)
	pg.draw.line(screen, BLACK, (750,0), (750,1000), 1)

def draw_lights(screen, traffic_lights, track):
	for light in traffic_lights:
		loc = light.loc
		if light.color == Color.green:
			color = GREEN
		elif light.color == Color.red:
			color = RED
		else:
			print "YELLO"
			color = YELLOW
		x,y = 0, 1000/loc

		#rect takes in x,y,width,height
		pg.draw.rect(screen, color, (x,y,1000,25))

def draw_cars(screen, cars, track):
	for car in cars:
		lane = car.lane
		loc = car.dist
		direction = car.direction
		x = 0
		if direction == Direction.right:
			x += 500
		if lane == 2:
			x += 250
		x+= 100
		y = 1000/(loc + 1)
		#rect takes in x,y,width,height
		pg.draw.rect(screen, BLUE, (x, y, 50, 1000/track.length))

def main():
		traffic_lights = [TrafficLight(20, Color.green, 10, 10, 10)]
		cars = [Car(2, 20, Direction.left, 1, False, 25)]
		track = Track(25, cars, traffic_lights, None, None)
		pg.init()
		screen = pg.display.set_mode((1000, 1000))
		pg.display.set_caption("Traffic Simulator")
		track_len = 100
		#fill with white
		done = False
		lane_width = 1000/4
		clock = pg.time.Clock()
		# agent = self.agent
		# If you want a background image, replace this clear with blit'ing the
	    # background image.
		screen.fill(GRAY)
	 
	    # --- Drawing code should go here
		pg.display.flip()
		# self.recording.append(self.start)
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

			# self.draw_agent(agent)
			# self.draw_boxes()
			# self.draw_rewards()
		    # --- Go ahead and update the screen with what we've drawn.
			# reward += self.reward_mat[agent.get_loc()]
			# self.recording.append(agent.get_loc())
			delay = 1000
			# if agent.get_loc() == self.goal:
			# 	delay = 1000
			# 	done = True
			# 	#save rewards
				#save recordings
			pg.display.flip()
		    # --- Limit to 60 frames per second
			clock.tick(60)
			pg.time.delay(delay)
			# wait

if __name__ == '__main__':
	main()