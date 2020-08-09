import pygame, sys, pickle
import random
from constants import *
from time import sleep

pygame.font.init()

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
	def __init__(self, i, j, width, height, color,color_name, heading, g):
		self.score = 0
		self.dead = False
		self.moving = True
		self.i = i
		self.j = j
		self.width = width
		self.height = height
		self.color = color
		self.color_name = color_name
		self.g = g
		self.rect = (g.grid[i][j].x, g.grid[i][j].y, width, height)
		self.heading = heading
		self.vel = 1
		self.body = []
		self.frame_count = 0
		self.frame_bound = 4

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
						self.deadly_collision()
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
						self.deadly_collision()
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
						self.deadly_collision()
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
						self.deadly_collision()
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

	def check_collision(self,a, eat_sound,s2):
		
		# checking with other snake
		if self.i == s2.i and self.j == s2.j:
			pass
		else:
			for b in s2.body:
				if b[0] == self.rect[0] and b[1] == self.rect[1]:
					self.deadly_collision()
				else:
					pass	


		# checking with apple			
		if a.i == self.i and a.j == self.j:
			a.visible = False
			self.score += 1
			a.eaten(eat_sound)
			self.add_body()
			a.change_pos(self.g)
			a.visible = True
			return True
		else:
			return False

	def deadly_collision(self):

		self.moving = False
		self.dead = True

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
		self.image = None
		self.change_pos(self.g)


	def update(self):
		self.rect = (self.x, self.y,)

	def draw(self,win, image_surface):
		if self.visible:
			self.update()
			# pygame.draw.rect(win,self.color,self.rect)
			win.blit(image_surface , self.rect)

	def change_pos(self,g):
		self.i = random.randint(0,rows-1)
		self.j = random.randint(0,cols-1)
		self.cell = g.grid[self.i][self.j]
		self.x = self.cell.x
		self.y = self.cell.y
		self.update()

	def eaten(self,eat_sound):
		eat_sound.play()	




class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.snakes = [0,0]
        self.alive = [True , True]
        self.a = None
        self.g = None
        
    def connected(self):
        return self.ready


def custom_encode(data,mode):
	if mode == "pickle":
		# print("encoding pickled data")
		data = pickle.dumps(data)
		data = bytes(f"{len(data):<{HEADERSIZE}}" , "utf-8")+data		
		return data

	elif mode == "string":
		data = bytes(f"{len(data):<{HEADERSIZE}}"+data , "utf-8")		
		return data



def custom_recv_decode(conn, mode):
	if mode == "pickle":
		
		full_msg = b""
		new_msg = True

		while True:
			
			try:
				msg = conn.recv(4096)
			except Exception as e:
				print(e)
			if new_msg:
				#print("Printing header of recv data",msg[:HEADERSIZE])
				try:
					msglen = int(msg[:HEADERSIZE])
				except:
					return -1	
				new_msg = False

			full_msg += msg

			if len(full_msg)-HEADERSIZE == msglen:
				
				return pickle.loads(full_msg[HEADERSIZE:])

	
	elif mode == "string":
		full_msg = b""
		new_msg = True

		while True:
			msg = conn.recv(4096)
			if new_msg:
				msglen = msg[:HEADERSIZE]	
				new_msg = False

			full_msg += msg

			if len(full_msg)-HEADERSIZE == msglen:
				return full_msg[HEADERSIZE:].decode("utf-8") 

class EndScreen():
	def __init__(self,won,msg,s1,s2):
		self.won = won
		self.msg = msg
		self.s1 = s1
		self.s2 = s2
		if self.won:
			#won
			self.t = Text("You Won The Game!!!!", green, 35,height/2 -100)

		else:
			#lost
			self.t = Text("You Lost The Game....", red, 35,height/2 -100)

		self.score = Text("Your Score : "+str(s1.score)+"    "+"Oponent Score : "+str(s2.score),black , 35 , height/2)	
		self.press_enter = Text("Please Press Enter To Restart", green, 35,height/2 +100)



	def draw(self,win):
		win.fill(white)
		self.t.draw(win)
		self.score.draw(win)
		self.press_enter.draw(win)

		pygame.display.update()

	def wait_key_press(self,win):

		draw_end = True
		while draw_end:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menu_run = False
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN :
					if event.key == pygame.K_RETURN:
						print("breaking out")
						draw_end = False
						break

			self.draw(win)		

class Text():
	def __init__(self, text, color, size, y_shift):
		self.text = text
		self.color = color
		self.size = size
		self.y_shift = y_shift
		self.font = pygame.font.Font("assets/Purisa.ttf", self.size)
		self.screen_text = self.font.render(self.text , True, self.color)
		self.rect = self.screen_text.get_rect()
		self.x = round(width/2) - round(self.rect.width/2) 
		self.y = self.y_shift
		self.width = self.rect.width
		self.height = self.rect.height
		self.display = True
	def draw(self,win):
		if self.display:
			win.blit(self.screen_text, (self.x, self.y))	





