import threading, socket, select, json, queue

class Chat_Server:
	def __init__(self):
		self.conns = set() # all connections
		self.actives = set() # connections who provided an username
		self.data = {} # all data we want to store
		self.print_queue = queue.Queue()
		t = threading.Thread(target=self.print_manager)
		t.daemon = True
		t.start()
		del t

	def print_manager(self):
		while True:
			msg = self.print_queue.get()
			print(msg)
			self.print_queue.task_done()

	def run(self, addr, port):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock.bind((addr, port))
			sock.listen(5)
			self.print_queue.put('Server started at {}:{}\n'.format(addr, port))
			while True:
				client, addr = sock.accept()
				self.conns.add(client)
				self.print_queue.put("New Connection: {}\nConnections {}: {}\n\n".format(addr, len(self.conns), self.conns))
				t = threading.Thread(target=self.server_handler, args=(client,), name='t_{}'.format(self.client_name(client)))
				t.start()

	def client_name(self, client):
		return ':'.join(str(i) for i in client.getpeername())

	def has_username(self, client):
		return self.data[self.client_name(client)]['username'] is not None

	def client_close(self, client):
		self.print_queue.put('\n[-] Client {} ({}) closed the conection'.format(client.getpeername(), self.data[self.client_name(client)]))
		self.conns.remove(client)
		del self.data[self.client_name(client)]
		if(client in self.actives):
			self.actives.remove(client)
		self.print_queue.put("[-] Connections ({}): {}\n[-] Actives ({}): {}\n\n".format(len(self.conns), self.conns, len(self.actives), self.actives))

	def send_msg(self, msg, sender, to, from_server=False):
		to_send = {'from': sender, 'message': msg, 'msg_from_server': from_server}
		to.send(json.dumps(to_send).encode('utf-8'))

	def show_report(self, raw, req, client):
		recipients = ', '.join(self.data[self.client_name(i)]['username'] for i in self.actives if i is not client)
		report_msg = '[+] Thread: {}\n[+] Message sent from {} to: {}\n[+] Content: {} ({})'
		report = report_msg.format(threading.currentThread().getName(), self.data[self.client_name(client)]['username'], recipients, raw, req)
		end_output = '{}\n[+] Total data: {}\n\n'.format(report, self.data)
		self.print_queue.put(end_output)

	def send_to_all(self, msg, client, sender, from_server=False):
		if(not from_server):
			self.data[self.client_name(client)]['msgs_sent'].append(msg)
		ready_to_read,ready_to_write,in_error = select.select(self.actives, self.actives,[],0)
		for sock_write in ready_to_write:
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
			self.show_report(raw, req, client)


chat = Chat_Server()
chat.run('', 9005) # adjust host/port
