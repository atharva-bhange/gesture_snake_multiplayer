import socket, pickle


class Network():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.server =  "192.168.1.131"
		self.port = 5555
		self.addr = (self.server , self.port)
		self.game = self.connect()

	def connect(self):
		try:
			self.client.connect(self.addr)	
			data = []
			count = 0
			while True:
				if count > 50:
					return "bla"
				count += 1
				packet = self.client.recv(4096)
				if not packet: break
				data.append(packet)			
			self.game = pickle.loads(b"".join(data))	
			return self.game

		except Exception as e:
			print("couldn't connect" , e)

	def send(self, send_data):
		try:
			self.client.send(pickle.dumps(send_data))
			print("sent")
			data = []
			count = 0
			while True:
				if count > 50:
					print("recv data slow")
					return self.game
				count += 1
				packet = self.client.recv(4096)
				if not packet: break
				data.append(packet)		
			self.game = pickle.loads(b"".join(data))	 	
			return 	self.game
		except Exception as e:
			print(e)



