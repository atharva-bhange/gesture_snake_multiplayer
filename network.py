import socket, pickle
from newconstants import *
from components import *


# class Network():
# 	def __init__(self):
# 		self.client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# 		self.server =  socket.gethostname()
# 		self.port = 5555
# 		self.addr = (self.server , self.port)
# 		self.game = self.connect()

# 	def connect(self):
# 		try:
# 			self.client.connect(self.addr)	
# 			full_msg = b""
# 			new_msg = True

# 			while True:
# 				msg = self.client.recv(1024)
# 				if new_msg:
# 					msglen = msg[:HEADERSIZE]
# 					new_msg = False

# 				full_msg += msg

# 				if len(full_msg)-HEADERSIZE == msglen:
# 					self.game = pickle.loads(full_msg[HEADERSIZE:])
# 					break

# 			return self.game

# 		except Exception as e:
# 			print("couldn't connect" , e)

# 	def send(self, send_data):
# 		try:
# 			data = pickle.dumps(send_data)
# 			data = bytes(f"{len(data):<{HEADERSIZE}}" , "utf-8")+data
# 			self.client.send(data)

# 			full_msg = b""
# 			new_msg = True

# 			while True:
# 				msg = self.client.recv(1024)
# 				if new_msg:
# 					msglen = msg[:HEADERSIZE]
# 					new_msg = False

# 				full_msg += msg

# 				if len(full_msg)-HEADERSIZE == msglen:
# 					self.game = pickle.loads(full_msg[HEADERSIZE:])
# 					break

# 			return self.game

# 		except Exception as e:
# 			print(e)


class Network():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.server =  socket.gethostname()
		self.port = 5555
		self.addr = (self.server , self.port)

	def connect(self):
		try:
			self.client.connect(self.addr)	
			return custom_recv_decode(self.client , 'pickle')

		except Exception as e:
			print( e)

	def send(self, send_data):
		try:
			encoded_data =  custom_encode(send_data,'pickle')
			self.client.send(encoded_data)

			return custom_recv_decode(self.client , 'pickle')
		except Exception as e:
			print(e)


