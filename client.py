"""It is a simple data exchange program,
based on the TCP protocol.
With this program you can exchange data on your local network
"""

import socket

SERVER_IP = input("IP address: ")
SERVER_PORT = int(input("Port number: "))
SIZE = 1024  #size of packages


class Client_socket_TCP():
	"""
	This class implements the client side of the program
	"""
	def __init__(self):
		"""create connection with server"""
		self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client_socket.connect((SERVER_IP,SERVER_PORT))

	def send_text_data(self,text):
		"""this function send text data to the server"""
		self.client_socket.send(text)

	def open_file(self,path):
		"""just open file,nothing more"""
		with open(path,"rb") as file:
			data = file.read()
		return data

	def from_decimal_to_hex(self,number):
		"""converts a number from decimal to hex"""
		hex_number = (number).to_bytes(4,byteorder = "big")
		return hex_number

	def bytes_separation(self,data):
		"""this is main function in this class, it separate data, send it to the server 
		and checks errors"""
		low = 0
		high = 2**10 - 6
		number_of_packet = 0

		while True:
			hex_number = self.from_decimal_to_hex(number_of_packet)

			if len(data[low:high]) == 1018:
				self.client_socket.send(data[low:high] + b" 0" + hex_number)
			else:
				print(len(data[low:high]))
				self.client_socket.send(data[low:high] + b" 1" + hex_number)
				break

			while True:
				responce = self.client_socket.recv(SIZE)

				if responce == b"ERROR." and len(data[low:high]) == 1018:
					print(responce.decode())
					self.client_socket.send(data[low:high] + b" 0" + hex_number)
				elif responce == b"ERROR." and len(data[low:high]) != 1018:
					print(responce.decode())
					self.client_socket.send(data[low:high] + b" 1" + hex_number)
				elif responce == b"OK.":
					break

			number_of_packet += 1
			low += 2**10 - 6
			high += 2**10 - 6

	def send_bytes_data(self,path):
		"""send name of file and call bytes_separation"""
		name = path.split("\\")[-1]
		self.send_text_data(name.encode())

		data = self.open_file(path)
		self.bytes_separation(data)

	def close(self):
		"""close connection"""
		self.client_socket.close()



def main():
	"""this is main loop"""
	soc_obj = Client_socket_TCP()
	choice = int(input("""Select an action:
0 - Exit
1 - Send a text message
2 - Send byte message
>>"""))
	while choice != 0:
		if choice == 1:
			soc_obj.send_text_data(b"Text.")
			text = input("Enter text:\n>>").encode()
			soc_obj.send_text_data(text)
		elif choice == 2:
			soc_obj.send_text_data(b"Bytes.")
			path = input("Enter the full path to the file:\n>>").replace("\\","\\")
			soc_obj.send_bytes_data(path)
		choice = int(input("""Select an action:
0 - Exit
1 - Send a text message
2 - Send byte message
>>"""))
	else:
		soc_obj.send_text_data(b"End.")
		soc_obj.close()


main()
