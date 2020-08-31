import socket
import select

HEADER_LENGHT = 10
IP = "192.168.24.007"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LENGHT)

		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8').strip())
		return {"header": message_header, "data": client_socket.recv(message_length)}


	except:
		return False

while True:
	read_sockets, _, exeption_sockets = select.select(sockets_list, [], sockets_list)

	for notified_socket in read_sockets:
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()

			user = receive_message(client_socket)
			if user is False:
				continue
			sockets_list.append(client_socket)

			clients[client_socket] = user

			print(f"Nouvelle connexion acceptée depuis {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

		else:
			message = receive_message(notified_socket)

			if message is False:
				print(f"Connexion fermée depuis {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue
			
			user = clients[notified_socket]
			print(f"Message reçu de la part de :{user['data'].decode('data')}: {message['data'].decode('utf-8')}")

			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user["header"] + user['data'] + message['header'] + message['data'])

	for notified_socket in exeption_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]















