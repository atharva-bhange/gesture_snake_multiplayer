import pygame, sys
import random
from newconstants import *


class wall():
	def __init__(self,x,y,width,height,color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.rect = (x, y, width, height)

	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

	def draw(self,win):
		pygame.draw.rect(win,self.color,self.rect)

class cell():
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.color = (0,255,0)
		self.width = width
		self.height = height
		self.rect = (x, y, width, height)

	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

	def draw(self,win):
		pygame.draw.rect(win,self.color,self.rect)


class Grid():
	def __init__(self, rows,cols):
		self.rows = rows
		self.cols = cols

		self.make_grid()

	def make_grid(self):
		self.grid = [[0 for i in range(self.cols)] for j in range(self.rows)]

class Snake():
	def __init__(self, i, j, width, height, color, heading, g):
		self.score = 0
		self.moving = True
		self.i = i
		self.j = j
		self.width = width
		self.height = height
		self.color = color
		self.g = g
		self.rect = (g.grid[i][j].x, g.grid[i][j].y, width, height)
		self.heading = heading
		self.vel = 1
		self.body = []
		self.frame_count = 0
		self.frame_bound = 5

	def move(self):
		if self.moving:
			keys = pygame.key.get_pressed()

			old_heading = self.heading

			# Changing heading of the snake		
			if keys[pygame.K_LEFT] and old_heading != 'R' and old_heading != 'L':
				self.heading = 'L'
			elif keys[pygame.K_RIGHT] and old_heading != 'L' and old_heading != 'R':
				self.heading = 'R'
			elif keys[pygame.K_UP] and old_heading != 'D' and old_heading != 'U':
				self.heading = 'U'
			elif keys[pygame.K_DOWN] and old_heading != 'U' and old_heading != 'D':
				self.heading = 'D'

			old_rect = self.rect

			# Continuously moving the snake
			if self.heading == 'L':
				if self.frame_count >= self.frame_bound:
					if self.j == 0:
						self.wall_collision()
						return
					else: 
						self.j -= self.vel
						self.update(old_rect)
						self.frame_count = 0
				else:
					self.frame_count += 1
			elif self.heading == 'U':
				if self.frame_count >= self.frame_bound:
					if self.i == 0:
						self.wall_collision()
						return
					else:
						self.i -= self.vel
						self.update(old_rect)
						self.frame_count = 0
				else:
					self.frame_count += 1
			elif self.heading == 'R':		
				if self.frame_count >= self.frame_bound:
					if self.j == cols-1:
						self.wall_collision()
						return
					else:
						self.j += self.vel
						self.update(old_rect)
						self.frame_count = 0
				else:
					self.frame_count += 1
			else:	
				if self.frame_count >= self.frame_bound:
					if self.i == rows-1:
						self.wall_collision()
						return
					else:
						self.i += self.vel
						self.update(old_rect)
						self.frame_count = 0
				else:
					self.frame_count += 1	

	def update(self,old_rect):
		
		self.rect = (self.g.grid[self.i][self.j].x, self.g.grid[self.i][self.j].y, self.width, self.height)
		self.move_body(old_rect)

	def draw(self,win):
		pygame.draw.rect(win,self.color,self.rect,)
		if self.heading == 'U':
			pygame.draw.rect(win,white,(self.rect[0]+4,self.rect[1]+4,4,4))
			pygame.draw.rect(win,white,(self.rect[0]+12,self.rect[1]+4,4,4))
		elif self.heading == 'R':
			pygame.draw.rect(win,white,(self.rect[0]+12,self.rect[1]+4,4,4))
			pygame.draw.rect(win,white,(self.rect[0]+12,self.rect[1]+12,4,4))
		elif self.heading == 'D':
			pygame.draw.rect(win,white,(self.rect[0]+4,self.rect[1]+12,4,4))
			pygame.draw.rect(win,white,(self.rect[0]+12,self.rect[1]+12,4,4))
		else:
			pygame.draw.rect(win,white,(self.rect[0]+4,self.rect[1]+4,4,4))
			pygame.draw.rect(win,white,(self.rect[0]+4,self.rect[1]+12,4,4))
		for i in self.body:
			pygame.draw.rect(win,self.color,i)

	def check_collision(self,a):
		# checking with apple
		if a.i == self.i and a.j == self.j:
			a.visible = False
			self.score += 1
			self.add_body()
			a.change_pos(self.g)
			a.visible = True

	def wall_collision(self):
		self.moving = False

	def add_body(self):
		self.body.append(self.rect)



	def move_body(self, old_rect):
		if self.body:
			for i in range(len(self.body)-1 , 0 , -1):
				self.body[i] = self.body[i-1]
			self.body[0] = old_rect		


class Apple():
	def __init__(self, g):
		self.visible = True
		self.width = 24
		self.height = 24
		self.color = (255,0,0)
		self.rect = (0,0, 20, 20)
		self.g = g
		self.cell = 0
		self.change_pos(self.g)


	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

	def draw(self,win):
		if self.visible:
			self.update()
			pygame.draw.rect(win,self.color,self.rect)

	def change_pos(self,g):
		self.i = random.randint(0,rows-1)
		self.j = random.randint(0,cols-1)
		self.cell = g.grid[self.i][self.j]
		self.x = self.cell.x
		self.y = self.cell.y

class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.snakes = [0,0]
        self.s0_alive = False
        self.s1_alive = False
        self.g = None
        
    def connected(self):
        return self.ready


