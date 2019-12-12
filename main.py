import pygame as pg
from pygame.locals import *
import sys
import math

SCREENSIZE = 720

screen = pg.display.set_mode((720,720), HWACCEL|HWSURFACE|DOUBLEBUF)


DAMPENING = 0.8
DAMPENING_A = 0.8
INCHES = 144
PIX_PER_INCH = SCREENSIZE//INCHES

class Robot:
	def __init__(self):
		self.width = 18
		self.enc_di = 1

		self.x = 0
		self.y = 0
		self.a = 0

		self.vel_x = 0
		self.vel_y = 0
		self.vel_a = 0

		self.enc_l = 0
		self.enc_r = 0
		self.enc_c = 0

		self.paths = []

		self.odo_x = 0
		self.odo_y = 0
		self.odo_a = 0
	
	def update(self, keys):
		
		if keys[K_UP]:
			self.vel_x += math.cos(self.a)/2
			self.vel_y += math.sin(self.a)/2
		if keys[K_DOWN]:
			self.vel_x += math.cos(self.a+(math.pi))/2
			self.vel_y += math.sin(self.a+(math.pi))/2
		if keys[K_LEFT]:
			self.vel_x += math.cos(self.a-(math.pi/2))/2
			self.vel_y += math.sin(self.a-(math.pi/2))/2
		if keys[K_RIGHT]:
			self.vel_x += math.cos(self.a+(math.pi/2))/2
			self.vel_y += math.sin(self.a+(math.pi/2))/2

		if keys[K_a]:
			self.vel_a -= 0.05/2
		if keys[K_d]:
			self.vel_a += 0.05/2

		self.vel_a += (random.randint(-100,100)/1000000*math.sqrt(self.vel_x**2+self.vel_y**2))
		self.a += self.vel_a/2  

		self.enc_c -= (self.vel_x*math.sin(self.a))-(self.vel_y*math.cos(self.a))
		self.enc_l += (self.vel_x*math.cos(self.a))+(self.vel_y*math.sin(self.a)) + (((self.vel_a)/(2*math.pi))*(self.width*math.pi)) 
		self.enc_r += (self.vel_x*math.cos(self.a))+(self.vel_y*math.sin(self.a)) - (((self.vel_a)/(2*math.pi))*(self.width*math.pi))

		self.x += self.vel_x
		self.y += self.vel_y
		self.a += self.vel_a/2
		#print(self.enc_c, self.enc_l, self.enc_r)



		self.vel_x *= DAMPENING
		self.vel_y *= DAMPENING
		self.vel_a *= DAMPENING_A


	def path(self):
		old = (self.odo_x, self.odo_y, self.odo_a)

		"""
		self.odo_a += (self.enc_l-self.enc_r)/self.width

		p = (self.enc_r+self.enc_l)/2
		n = self.enc_c

		self.odo_y += ((p * math.sin(self.odo_a)) + (n * math.cos(self.odo_a)))
		self.odo_x += ((p * math.cos(self.odo_a)) - (n * math.sin(self.odo_a)))
		"""
		"""
		dc = ((self.enc_r + self.enc_l) / 2)
		ph = (self.enc_l - self.enc_r) / self.width

		self.odo_x += dc * math.cos(self.odo_a + (ph / 2))
		self.odo_y += dc * math.sin(self.odo_a + (ph / 2))
		self.odo_a += ph
		"""
	
		dc = ((self.enc_r + self.enc_l) / 2)
		ph = (self.enc_l - self.enc_r) / self.width

		self.odo_x += dc * math.cos(self.odo_a + (ph / 2)) - self.enc_c * math.sin(self.odo_a + (ph / 2))
		self.odo_y += dc * math.sin(self.odo_a + (ph / 2)) + self.enc_c * math.cos(self.odo_a + (ph / 2))
		self.odo_a += ph


		"""
		self.odo_a = self.a #! getting angle by gyro

		xc = self.enc_c
		yc = (self.enc_l+self.enc_r)/2

		xe = [0,0]
		ye = [0,0]

		xe[0] = xc*math.sin(self.odo_a)
		ye[0] = yc*math.cos(self.odo_a)

		xe[1] = xc*math.cos(self.odo_a)
		ye[1] = yc*math.sin(self.odo_a)

		self.odo_x += xe[0] + ye[0]
		self.odo_y += xe[1] + ye[1]
		"""
		
		"""
		theta = (self.enc_l - self.enc_r) / self.width
		xi = self.enc_c
		yi = (self.enc_l + self.enc_r) / 2
		r = yi / theta
		r2 = xi / theta
		dx = r - math.cos(theta) * r + r2 * math.sin(theta)
		dy = r * math.sin(theta) + r2 - r2 * math.cos(theta)
		self.odo_x += math.cos(self.odo_a) * (dy + dx)
		self.odo_y += math.sin(self.odo_a) * (dy + dx)
		self.odo_a += theta
		"""
		"""
		theta = (self.enc_l - self.enc_r) / self.width
		xi = self.enc_c
		yi = (self.enc_l + self.enc_r) / 2

		dx = 0
		dy = 0

		if theta == 0:
			dx = xi
			dy = yi
		else:
			r = yi / theta
			r2 = xi / theta
			dx = r - math.cos(theta) * r + r2 * math.sin(theta)
			dy = r * math.sin(theta) + r2 - r2 * math.cos(theta)

		self.odo_x += math.cos(self.odo_a) * dy + math.sin(self.odo_a) * dx
		self.odo_y += math.sin(self.odo_a) * dy + math.cos(self.odo_a) * dx
		self.odo_a += theta
		"""
		"""
		xi = self.enc_c
		yi = (self.enc_l + self.enc_r) / 2
		theta = (self.enc_l - self.enc_r) / self.width

		sineTerm = math.sin(theta) / theta if theta else 1
		cosTerm = (1 - math.cos(theta)) / theta if theta else 0
		dx = xi * sineTerm - yi * cosTerm
		dy = xi * cosTerm + yi * sineTerm
		self.odo_y += dx * math.cos(self.odo_a) - dy * math.sin(self.odo_a)
		self.odo_x += dx * math.sin(self.odo_a) + dy * math.cos(self.odo_a)
		self.odo_a -= theta
		"""
		#print(self.enc_c, self.enc_l, self.enc_r)

		#print("ODO:", self.odo_x, self.odo_y, self.odo_a)

		#print((abs(self.vel_x)+abs(self.vel_y))*30/12/1.467)

		new = (self.odo_x, self.odo_y, self.odo_a)

		self.paths.append([old, new])

		self.enc_c = 0
		self.enc_l = 0
		self.enc_r = 0

	def draw(self, surf):
		pg.draw.circle(surf, (50,50,255), (int(self.x*PIX_PER_INCH),int(self.y*PIX_PER_INCH)), int(self.width/2*PIX_PER_INCH), 2)
		pg.draw.line(surf, (50,255,50), (int(self.x*PIX_PER_INCH),int(self.y*PIX_PER_INCH)), (int((self.x+(math.cos(self.a)*14))*PIX_PER_INCH),int((self.y+(math.sin(self.a)*14))*PIX_PER_INCH)), 2)
		for path in self.paths:
			pg.draw.line(surf, (255,50,50), (int(path[0][0]*PIX_PER_INCH),int(path[0][1]*PIX_PER_INCH)), (int(path[1][0]*PIX_PER_INCH),int(path[1][1]*PIX_PER_INCH)), 2)

robot = Robot()

clock = pg.time.Clock()

f = 0

import random

while 1:
	for event in pg.event.get():
		if event.type == QUIT:
			sys.exit()

	keys = pg.key.get_pressed()

	robot.update(keys)

	if f % 1 == 0:
		robot.path()

	screen.fill((0,0,0))

	robot.draw(screen)
	pg.display.flip()

	clock.tick(60)
	f+=1