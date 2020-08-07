import socket 
import pickle 
from _thread import * 
from components import *


HEADERSIZE = 10
id_count = 0
games = {}
conn = None


G = Grid(rows, cols)

start_x = wall_thickness
start_y = wall_thickness

for i in range(0 , G.rows):
	for j in range(0, G.cols):
		G.grid[i][j] = cell(start_x , start_y, cell_thickness,cell_thickness)
		start_x += cell_thickness + partition_thickness
	start_x = wall_thickness
	start_y += cell_thickness + partition_thickness



def threaded_client(conn , p, game_id):
	global id_count, games
	print("threaded client created")

	if p == 0 :
		color = random.choice(clr_list_1)
		games[game_id].snakes[p] = Snake(random.randint(3,rows//2),random.randint(3,cols//2),snake_head_width,snake_head_height,color,str(color),random.choice(headings),G)
	else:
		games[game_id].ready = True
		games[game_id].a = Apple(G)
		games[game_id].g = G
		color = random.choice(clr_list_2)
		games[game_id].snakes[p] = Snake(random.randint(rows//2 + 1, rows - 4),random.randint(cols//2 +1,cols - 4),snake_head_width,snake_head_height,color,str(color),random.choice(headings),G)


	intial_data =  custom_encode( {'game' : games[game_id] , 'id' :str(p)} , "pickle")

	try:
		conn.send(intial_data)
	except Exception as e:
		print(e)

	while True:
		try:
			try:
				recieved_data = custom_recv_decode(conn, "pickle")
			except:
				break
				

			if game_id in games:
				game = games[game_id]

				if not recieved_data:
					print("exited threaded loop because no dat recieved")																																					
					break
				else:
					
					try:
						if recieved_data == 'fetch':

							try:
								send_data = custom_encode(games[game_id] , "pickle")
								conn.send(send_data)
							except:
								break		
						elif recieved_data == 'killgame':
							games[game_id].alive[p] = False 
							try:
								send_data = custom_encode(games[game_id] , "pickle")
								conn.send(send_data)
							except:
								break
														
							break	
						else:
							if recieved_data['apple_collision_status']:
								games[game_id].snakes[p] = recieved_data['snake']
								games[game_id].a = recieved_data['apple']
							else:
								games[game_id].snakes[p] = recieved_data['snake']

							if recieved_data['snake'].dead:
								games[game_id].alive[p] = False	

							try:	
								send_data = custom_encode(games[game_id] , "pickle")
								conn.send(send_data)
							except:
								break			

						 		

						# Send data



						if games[game_id].alive[0] == False or games[game_id] == False:
							break
					except :
						break	
			else:
				print("no game")
				break
		except Exception as e:
			print('massive exception')
			break	

	print("Lost connection from ", p)
	try:
		del games[game_id]
		print("Closing Game", game_id)
	except:
		pass
	id_count -= 1

	conn.close()


s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
try:
	s.bind((server, port))
except:
	exit()	


s.listen(5)
print("Server Started at ip", server ,"and port" , port)

while True:

	try:
		conn, address = s.accept()
		print(f"Connection from {address} is established")

		id_count += 1
		p = 0 

		# We are trying to determine which game should a client be assigned to
		game_id = (id_count - 1) // 2


		# A game doesn't exist for this client 
		if id_count % 2 == 1:
			games[game_id] = Game(game_id)
			print("Creating a new game")

		# game exists for this client and joining it
		else:
			print("Joing on going game")
			p = 1		

		start_new_thread(threaded_client, (conn,p,game_id))




	except KeyboardInterrupt as e:
		if conn != None:
			conn.close()
		break  

