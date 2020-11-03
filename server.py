"""It is a simple data exchange program,
based on the TCP protocol.
With this program you can exchange data on your local network

Packages description:
Each package is 1 kilobyte in size
					Consists
			|							|
1018 bytes  |	two bytes				|	Number of package
of data 	|	" " + and byte 			|	four bytes
			|	(1-end,0-not the end)	|


"""


import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
SIZE = 1024


class Server_socket_TCP():
	"""
	This class implements the server side of the program
	"""
	def __init__(self):
		"""create server socket"""
		self.serv_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.serv_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.client_socket = self.socket_initialization()

	def socket_initialization(self):
		"""accept connection from client"""
		self.serv_socket.bind((SERVER_IP,SERVER_PORT))
		self.serv_socket.listen()
		client_socket,address = self.serv_socket.accept()
		print("Connection from",address)
		return client_socket

	def get_text_data(self):
		"""take text data from client"""
		data = self.client_socket.recv(SIZE).decode()
		return data

	def hex_to_decimal(self,byte):
		"""converts a number from hex to decimal"""
		number = int.from_bytes(byte,byteorder = "big")
		return number

	def get_bytes_data(self):
		"""this is main function in this class, it take bytes data
		and send errors"""
		name = self.get_text_data()

		end = False
		data = b""
		data_buffer = {}

		while True:
			responce = self.client_socket.recv(SIZE)

			while True:
				if responce[-6:-4] == b" 0" and len(responce) != 1024:
					print("Was transferred {} bytes".format(len(responce)))
					self.client_socket.send(b"ERROR.")
					break
				elif responce[1018:1020] == b" 0" and len(responce) == 1024:
					self.client_socket.send(b"OK.")
					data_buffer[self.hex_to_decimal(responce[1020:1024])] = responce[:1018]
					break
				elif responce[len(responce) - 6:len(responce) - 4] == b" 1":
					data_buffer[self.hex_to_decimal(responce[len(responce) - 4:len(responce)])] = responce[:1018]
					end = True
					break

			if end == True:
				break

		for i in range(len(data_buffer)):
			data += data_buffer[i]
			del data_buffer[i]

		return (data,name)



def main():
	"""this is main loop"""
	soc_obj = Server_socket_TCP()
	choice = soc_obj.get_text_data()

	while choice != "End.":
		if choice == "Text.":
			text = soc_obj.get_text_data()
			print(text)
		elif choice == "Bytes.":
			data,name = soc_obj.get_bytes_data()
			with open(r"C:\Users\admin\Pictures\Saved Pictures\{}".format(name),"wb") as file:
				file.write(data)
			print("File {} transferred!".format(name))

		data = b""
		try:
			choice = soc_obj.get_text_data()
		except ConnectionResetError:
			break

main()
print("Server is disconnecting...")
