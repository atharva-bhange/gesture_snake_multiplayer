import pygame, sys
import random
from newconstants import *
from components import *
from network import *


win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")


def redrawWindow(win, walls, s1,a):

	win.fill((173, 216, 230))
	for w in walls:
		w.draw(win)
	s1.draw(win)
	a.draw(win)
	pygame.display.update()

def main():
	main_run = True
	game_run = True 
	menu_run = True
	clock = pygame.time.Clock()

	while main_run:

		while menu_run:
			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menu_run = False
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN :
					if event.key == pygame.K_RETURN:
						n = Network()
						id = n.game.id
						
						G = n.game.g
						print(id)
						count = 0
						while True:
							if count > 50 :
								print(n.game)
								pygame.quit()
								sys.exit()
							count += 1
							n.game = n.send(game)
							if n.game.ready:
								break

						s1 = n.game.snake[id]
						s2 = n.game.snake[1 - id]
						menu_run = False


		walls = [wall(0,0,width, wall_thickness,wall_color),
		wall(0,0,wall_thickness,height,wall_color),
		wall(0,height-wall_thickness,width,wall_thickness,wall_color),
		wall(width-wall_thickness,0,wall_thickness,height,wall_color)]	

		start_x = wall_thickness
		start_y = wall_thickness

		while start_x < width - wall_thickness-cell_thickness:
			start_x += cell_thickness

			# Vertical wall
			vw = wall(start_x,wall_thickness,partition_thickness,height-(2*wall_thickness),partition_color)
			walls.append(vw)

			start_x += partition_thickness
			

		while start_y < height - wall_thickness-cell_thickness:
			start_y += cell_thickness

			# Horizontal wall
			hw = wall(wall_thickness,start_y,width-(2*wall_thickness),partition_thickness,partition_color)
			walls.append(hw)

			start_y += partition_thickness

		

		# start_x = wall_thickness
		# start_y = wall_thickness

		# for i in range(0 , G.rows):
		# 	for j in range(0, G.cols):
		# 		G.grid[i][j] = cell(start_x , start_y, cell_thickness,cell_thickness)
		# 		start_x += cell_thickness + partition_thickness
		# 	start_x = wall_thickness
		# 	start_y += cell_thickness + partition_thickness

		# s1 = s1 = Snake(3,3,snake_head_width,snake_head_height,(0,255,0),'R',G)
		a = Apple(G)


		while game_run:

			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_run = False
					pygame.quit()
					sys.exit()

			s1.check_collision(a)
			s1.move()
			redrawWindow(win,walls,s1,a)


main()
