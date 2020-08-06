# import socket, pickle
# from _thread import *
# from components import *



# server = socket.gethostname()
# port = 5555

# s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# print("Socket created")

# try:
# 	s.bind((server , port))
# except socket.error as e:
# 	str(e)

# s.listen()
# print("Waiting for connection Server started")

# connected = set()
# games = {}
# id_count = 0

# G = Grid(rows,cols)

# start_x = wall_thickness
# start_y = wall_thickness

# for i in range(0 , G.rows):
# 	for j in range(0, G.cols):
# 		G.grid[i][j] = cell(start_x , start_y, cell_thickness,cell_thickness)
# 		start_x += cell_thickness + partition_thickness
# 	start_x = wall_thickness
# 	start_y += cell_thickness + partition_thickness



# def threaded_client(conn, p, game_id):
# 	global id_count, games

# 	if p == 0 :
# 		games[game_id].snakes[p] = Snake(random.randint(3,rows//2),random.randint(3,cols//2),snake_head_width,snake_head_height,random.choice(clr_list_1),random.choice(headings),G)
# 	else:
# 		games[game_id].snakes[p] = Snake(random.randint(rows//2 + 1, rows - 4),random.randint(cols//2 +1,cols - 4),snake_head_width,snake_head_height,random.choice(clr_list_2),random.choice(headings),G)

# 	games[game_id].g = G	
# 	games[game_id].id = p	

# 	initial_data = pickle.dumps(games[game_id])
# 	initial_data = bytes(f"{len(initial_data):<{HEADERSIZE}}" , "utf-8")+initial_data
# 	conn.send(initial_data)

# 	reply = ""

# 	while True:
# 		try:
# 			# recv data
# 			full_msg = b""
# 			new_msg = True

# 			while True:
# 				msg = conn.recv(1024)
# 				if new_msg:
# 					msglen = msg[:HEADERSIZE]
# 					new_msg = False

# 				full_msg += msg

# 				if len(full_msg)-HEADERSIZE == msglen:
# 					g = pickle.loads(full_msg[HEADERSIZE:])
# 					break

# 			games[game_id] =  g			

# 			if game_id in games:
# 				game = games[game_id]

# 				if not recieved_data:
# 					break
# 				else:

# 					# Send data

# 					data = pickle.dumps(games[game_id])
# 					data = bytes(f"{len(data):<{HEADERSIZE}}" , "utf-8")+data
# 					conn.send(data)					


# 			else:
# 				break
# 		except Exception as e:
# 			print(e)
# 			break

# 	print("Lost connection")
# 	try:
# 		del games[game_id]
# 		print("Closing Game", game_id)
# 	except:
# 		pass
# 	id_count -= 1
# 	conn.close()



import socket 
import pickle 
import threading
from components import *
# from newconstants import *



HEADERSIZE = 10
threads = []
id_count = 0
games = {}
conn = None
port = 5555

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
	print(games,games[game_id].ready)


	if p == 0 :
		games[game_id].snakes[p] = Snake(random.randint(3,rows//2),random.randint(3,cols//2),snake_head_width,snake_head_height,random.choice(clr_list_1),random.choice(headings),G)
	else:
		games[game_id].ready = True
		games[game_id].a = Apple(G)
		games[game_id].g = G
		games[game_id].snakes[p] = Snake(random.randint(rows//2 + 1, rows - 4),random.randint(cols//2 +1,cols - 4),snake_head_width,snake_head_height,random.choice(clr_list_2),random.choice(headings),G)


	intial_data =  custom_encode( {'game' : games[game_id] , 'id' :str(p)} , "pickle")
	#print("initial send" , {'game_ready' : games[game_id].ready ,'game_id': games[game_id].id, 'id' :str(p)})

	try:
		conn.send(intial_data)
	except Exception as e:
		print(e)

	while True:
		try:
			#print(games)
			#print("inside threaded loop")
			try:
				recieved_data = custom_recv_decode(conn, "pickle")
				#print("recieving data" , recieved_data)
			except Exception as e :
				print("couldn't recv data" , e)

			if game_id in games.keys():
				game = games[game_id]

				if not recieved_data:
					print("exited threaded loop because no dat recieved")																																					
					break
				else:
					#print("In the else")
					if recieved_data == 'fetch':
						print(p ,"Only fetchin")
					else:
						if recieved_data['collision_status']:
							games[game_id].snakes[p] = recieved_data['snake']
							games[game_id].a = recieved_data['apple']
						else:
							games[game_id].snakes[p] = recieved_data['snake']


						# print("P0 rect " , games[game_id].boxes[0].rect)
						# print("P1 rect " , games[game_id].boxes[1].rect)
						
					#print("Recieved data : ", recieved_data)
					# Send data

					# data = pickle.dumps(games[game_id])
					# data = bytes(f"{len(data):<{HEADERSIZE}}" , "utf-8")+data
					# conn.send(data)				

					send_data = custom_encode(games[game_id] , "pickle")
					conn.send(send_data)	
					#print("Sending Data" , games[game_id])

			else:
				print("exited threaded loop because no game")
				break
		except Exception as e:
			print("exited threaded loop")
			print(e)
			break	

	print("Lost connection")
	try:
		del games[game_id]
		print("Closing Game", game_id)
	except:
		pass
	id_count -= 1
	conn.close()


s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((socket.gethostname(), port))



s.listen(5)
print("Server Started at port " , port)

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

		t = threading.Thread(target=threaded_client, args =(conn,p,game_id))
		t.start()
		threads.append(t)




	except KeyboardInterrupt as e:
		if conn != None:
			conn.close()
		break  

