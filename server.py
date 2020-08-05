import socket, pickle
from _thread import *
from components import *



server = "192.168.1.131"
port = 5555

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
print("Socket created")

try:
	s.bind((server , port))
except socket.error as e:
	str(e)

s.listen()
print("Waiting for connection Server started")

connected = set()
games = {}
id_count = 0

G = Grid(rows,cols)

start_x = wall_thickness
start_y = wall_thickness

for i in range(0 , G.rows):
	for j in range(0, G.cols):
		G.grid[i][j] = cell(start_x , start_y, cell_thickness,cell_thickness)
		start_x += cell_thickness + partition_thickness
	start_x = wall_thickness
	start_y += cell_thickness + partition_thickness



def threaded_client(conn, p, game_id):
	global id_count, games

	if p == 0 :
		games[game_id].snakes[p] = Snake(random.randint(3,rows//2),random.randint(3,cols//2),snake_head_width,snake_head_height,random.choice(clr_list_1),random.choice(headings),G)
	else:
		games[game_id].snakes[p] = Snake(random.randint(rows//2 + 1, rows - 4),random.randint(cols//2 +1,cols - 4),snake_head_width,snake_head_height,random.choice(clr_list_2),random.choice(headings),G)

	games[game_id].g = G	
	games[game_id].id = p	

	conn.send(pickle.dumps(games[game_id]))
	print(games[game_id].id)
	print(len(pickle.dumps(games[game_id], -1)))
	reply = ""

	while True:
		try:
			data = []
			while True:
				packet = conn.recv(4096)
				if not packet: 
					print("nopacket")
					break
				else:
					print("got packet")
				data.append(packet)			
			recieved_data =  pickle.loads(b"".join(data))
			print("Recieved data" , recieved_data)

			if game_id in games:
				game = games[game_id]

				if not recieved_data:
					break
					#pass
				else:
                    # if data == "reset":
                    #     game.resetWent()
                    # elif data != "get":
                    #     game.play(p, data)

					conn.sendall(pickle.dumps(games[game_id]))
					print("Sent data" , games[game_id])
					#pass
			else:
				break
		except:
			print("Problem with sending and recieving data")
			break

	print("Lost connection")
	try:
		del games[game_id]
		print("Closing Game", game_id)
	except:
		pass
	id_count -= 1
	conn.close()



while True:
	try:
		conn , addr = s.accept()
		print("Connnected to " , addr)

		id_count += 1
		p = 0 
		game_id = (id_count - 1) // 2

		if id_count % 2 == 1:
			games[game_id] = Game(game_id)
			print("Creating a new game")
		else:
			games[game_id].ready = True
			p = 1


		start_new_thread(threaded_client , (conn , p, game_id))

	except KeyboardInterrupt as e:
		if conn:  # <---
			conn.close()
		break  # <---


