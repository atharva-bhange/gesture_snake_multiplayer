import socket 
import pickle 
import threading
from newcomponents import *


HEADERSIZE = 10
threads = []
id_count = 0
games = {}
conn = None

def threaded_client(conn , p, game_id):
	global id_count, games
	print("threaded client created")
	print(games,games[game_id].ready)


	if p == 0:
		games[game_id].boxes[p] = Box(20,20,(255, 0 , 0))
	else:
		games[game_id].ready = True
		games[game_id].boxes[p] = Box(20,20,(0, 255 , 0))

	intial_data =  custom_encode( {'game' : games[game_id] , 'id' :str(p)} , "pickle")
	print("initial send" , {'game_ready' : games[game_id].ready ,'game_id': games[game_id].id, 'id' :str(p)})
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
						
						games[game_id].boxes[p] = recieved_data

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
s.bind((socket.gethostname(), 5555))



s.listen(5)
print("Server Started")

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
			print(game_id)
			games[game_id] = Game(game_id)
			print("Creating a new game")

		# game exists for this client and joining it
		else:
			print(game_id)
			# games[game_id].ready = True
			print("Joing on going game")
			print(games[game_id].ready)
			p = 1		

		t = threading.Thread(target=threaded_client, args =(conn,p,game_id))
		t.start()
		# start_new_thread(threaded_client , (conn , p, game_id))
		threads.append(t)




	except KeyboardInterrupt as e:
		if conn != None:
			conn.close()
		break  

