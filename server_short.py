import threading, socket, json

class Chat_Server:
	def __init__(self):
		self.conns = set() # all connections
		self.actives = set() # connections who provided an username
		self.data = {} # all data we want to store

	def run(self, addr, port):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock.bind((addr, port))
			sock.listen(5)
			print('Server started at {}:{}\n'.format(addr, port))
			while True:
				client, addr = sock.accept()
				self.conns.add(client)
				t = threading.Thread(target=self.server_handler, args=(client,), name='t_{}'.format(self.client_name(client)))
				t.start()

	def client_name(self, client):
		return ':'.join(str(i) for i in client.getpeername())

	def has_username(self, client):
		return self.data[self.client_name(client)]['username'] is not None

	def client_close(self, client):
		self.conns.remove(client)
		del self.data[self.client_name(client)]
		if(client in self.actives):
			self.actives.remove(client)

	def send_msg(self, msg, sender, to, from_server=False):
		to_send = {'from': sender, 'message': msg, 'msg_from_server': from_server}
		to.send(json.dumps(to_send).encode('utf-8'))

	def send_to_all(self, msg, client, sender, from_server=False):
		if(not from_server):
			self.data[self.client_name(client)]['msgs_sent'].append(msg)
		for sock_write in self.actives:
			if(sock_write is not client):
				self.send_msg(msg, sender, sock_write, from_server)

	def server_handler(self, client):
		self.data[self.client_name(client)] = {'msgs_sent': [], 'username': None}
		msg = 'welcome...{}.\nThere are this users connected: {}\n\n'
		msg = msg.format(client.getpeername(), [i.getpeername() for i in self.conns])
		self.send_msg(msg, 'SERVER', client, from_server = True)
		while True:
			try:
				raw = client.recv(1024)
				req = raw.decode('utf-8').strip()
			except Exception as err:
				break
			if(not req):
				self.client_close(client)
				break
			if(not self.has_username(client)):
				self.data[self.client_name(client)]['username'] = req
				self.send_to_all('{} HAS JOINED THE CHAT...'.format(req), client, 'SERVER', from_server = True)
				self.actives.add(client) # store all clients that gave an username
				continue
			self.send_to_all(req, client, self.data[self.client_name(client)]['username'])


chat = Chat_Server()
chat.run('', 9005) # adjust host/port
