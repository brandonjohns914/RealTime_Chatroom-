import socket
import threading
import sys

Port = 1234
IP= "127.0.0.1"
class Server:
    # creating TCP socket
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
 	#AF_INET internet address family #SOCK_STREAM = TCP 
	# list of whose joined the server
	connections_list = [] 
	def __init__(self):
		self.server_socket.bind((IP,Port)) #creates network and port
		self.server_socket.listen() # listen for clients trying to connect to the server
		print("Starting Brandon's Server: ")
		print("Waiting on others to join!")

	def connection_handler(self,connection_server,address_server):
		while True:
				data = connection_server.recv(2048).decode('utf-8') # Decoding the data as bytes
				data = f"{data}" #which client 
				print(data)
				connections = []
				for connect in self.connections_list:
					if not(connect == connection_server): #add to connections if not there
						connections.append(connect)
				for connection in connections: #send the data in bytes
						connection.send(bytes(data,'utf-8'))	
	
	def start_server(self):
		while True:
			connection,address = self.server_socket.accept() #blocks exe cution and waits for incoming connection
										            #server.accept() is the socket used to communicate with the client 

			print(f"{address} has connected.")
			#starting the connection thread 
			#passing the connection and the address of the socket back to connection handler to find a new connection 
			connection_thread = threading.Thread(target=self.connection_handler,args=(connection,address)) 
			connection_thread.daemon = True # running the thread in the background
			connection_thread.start() #connection thread to run 
			self.connections_list.append(connection) # Adding the new connection to the connections list


class Client:
    #socket object
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	def client_send_message(self):
		while True:
			message = input(f"{self.name} >> ")
			message = f"{self.name} > {message}"
			#converting message to bytes
			message = bytes(message,'utf-8')
			self.client_socket.send(message)

	def client_recieve_message(self):
		while True:
			message = self.client_socket.recv(2048).decode('utf-8')
			message = f"\n{message}"
			if message:
				print(str(message))

	def __init__(self,address):
		port = 1234
		self.client_socket.connect((address,port))
		self.name = input("Please enter your name : ")
		#signaling send message thread 
		send_thread = threading.Thread(target=self.client_send_message) 
		#  send message in the background
		send_thread.daemon = True 
		#signaling recieve message thread 
		recieve_thread = threading.Thread(target=self.client_recieve_message)
		#  recieve message in the background
		recieve_thread.daemon = True 
		#starting the threads 
		recieve_thread.start() 
		send_thread.start() 
		# recieve thread must finish first before send thread will start 
		recieve_thread.join()
		send_thread.join()
		while True:
			pass # An infinite loop that just keeps the two daemons running


if __name__ == "__main__":

	# counting arguements on command line  
	if len(sys.argv)>1: 
		client = None
		try:
			client = Client(sys.argv[1]) #client has 2 arguements 
		except Exception as error:
			print("Client Error")
		finally:
			if not(client==None):
				client.client_socket.close()
	else:
		server=None
		try:
			server = Server()
			server.start_server()
		except Exception as error:
			print("Server Error")
		finally:
			if not(server==None):
				server.server_socket.close()
		
