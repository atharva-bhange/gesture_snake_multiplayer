import  pygame, socket , pickle, sys
from newcomponents import *


width = 500
height = 500

win = pygame.display.set_mode((width,height))



def redrawWindow(win, b,b2):
	win.fill((255,255,255))
	b.update()
	b2.update()
	b.draw(win)

	b2.draw(win)
	pygame.display.update()




def main():
	clock = pygame.time.Clock()

	game_run = True
	menu_run = True

	while menu_run:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_run = False
				pygame.quit()
				sys.exit()		
			elif event.type == pygame.KEYDOWN :
				if event.key == pygame.K_RETURN:
					try:
						n = Network()
						info = n.connect()
						client_id = int(info['id'])
						print(client_id)
						game = info['game']

						while not game.ready:
							#print("Sending" , game)
							game = n.send('fetch')
							#print("Recieved " , game)

						menu_run = False
						b = game.boxes[client_id]
						b2 = game.boxes[1 - client_id]
						break


					except Exception as e:
						print(e)
						pygame.quit()
						sys.exit()


	while game_run:



		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_run = False
				pygame.quit()
				sys.exit()	



		b.move()		
		game.snakes[client_id] = b
		game = n.send(b)
		b2 = game.boxes[1 - client_id]
		redrawWindow(win , b, b2)	



main()