import pygame, socket,pickle

HEADERSIZE = 10

class Box():
	def __init__ (self,x,y,color):
		self.x = x
		self.y = y
		self.color = color
		self.width = 50
		self.height = 50
		self.rect = (x,y,50, 50)
		self.vel = 3

	def update(self):
		self.rect = (self.x,self.y,self.width, self.height)

	def draw(self, win):
		pygame.draw.rect(win,self.color,self.rect,)

	def move(self):

		keys = pygame.key.get_pressed()

	
		if keys[pygame.K_LEFT]:
			self.x -= self.vel
		elif keys[pygame.K_RIGHT]:
			self.x += self.vel
		elif keys[pygame.K_UP] :
			self.y -= self.vel
		elif keys[pygame.K_DOWN]:
			self.y += self.vel

		self.update()


class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.boxes = [0,0]
        self.s0_alive = False
        self.s1_alive = False
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
				msglen = int(msg[:HEADERSIZE])
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



