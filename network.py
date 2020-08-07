import socket, pickle
from constants import *
from components import *

class Network():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.server =  server
		self.port = port
		self.addr = (self.server , self.port)

	def connect(self):
		try:
			self.client.connect(self.addr)	
			recv = custom_recv_decode(self.client , 'pickle')
			if recv == -1:
				return -1
			else:	 
				return recv 

		except Exception as e:
			print( e)

	def send(self, send_data):
		try:
			encoded_data =  custom_encode(send_data,'pickle')
			self.client.send(encoded_data)
			recv = custom_recv_decode(self.client , 'pickle')
			if recv == -1:
				return -1
			else:	 
				return recv 
		except Exception as e:
			print(e)


