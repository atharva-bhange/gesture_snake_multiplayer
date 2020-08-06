import socket , pickle

HEADERSIZE = 10

s= socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect((socket.gethostname() , 5555))

while True:
	full_msg = b""
	new_msg = True

	while True:
		msg = s.recv(16)
		if new_msg:
			print(f"New msg lenght {msg[:HEADERSIZE]}")
			msglen = int(msg[:HEADERSIZE])
			new_msg = False

		full_msg += msg

		if len(full_msg)-HEADERSIZE == msglen:
			print("Full msg recvd")
			d = pickle.loads(full_msg[HEADERSIZE:])
			new_msg = True
			full_msg = ""
			break

	print(d)