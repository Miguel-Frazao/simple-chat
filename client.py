import socket, sys, select, json

class Client:
	def __init__(self):
		self.username = None

	def connect(self, host, port):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			try:
				print('Connecting to {} on port {}\n'.format(host, port))
				s.connect((host, port))
			except Exception as err:
				print('Unable to connect: {}'.format(err))
				sys.exit()
			self.begin_chat(s)

	def begin_chat(self, client_sock):
		while True:
			socket_list = [sys.stdin, client_sock]
			ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
			for sock in ready_to_read:
				if sock == client_sock:
					# message from server
					data = sock.recv(4096)
					if not data:
						print('\nDisconnected from chat server')
						sys.exit()
					else:
						data = json.loads(data.decode('utf-8'))
						color = '\033[1;32;40m'
						if(data['from'] == 'SERVER'):
							color = '\033[1;30;40m'
						output = '\r{}[{}]: {}\033[0;37;40m \n'.format(color, data['from'], data['message'])
						sys.stdout.write(output)
						if(self.username is None):
							sys.stdout.write('Your username?\n')
							sys.stdout.flush()
							continue
						sys.stdout.write('\033[1;34;40m[ME]:\033[0;37;40m ')
						sys.stdout.flush()
				else:
					#send message to server
					msg = sys.stdin.readline()
					if(msg.strip() != ''):
						if(self.username is None):
							self.username = msg
						client_sock.send(msg.encode('utf-8'))
					sys.stdout.write('\033[1;34;40m[Me]:\033[0;37;40m ')
					sys.stdout.flush()


client = Client()
client.connect('', 9005) # adjust host/port
