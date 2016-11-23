# simple-chat-python3

This is a simple socket based chat made in python 3.5.2

I could do this with `sys.argv` arguments, you can adjust host/port on the code, i thought it would be more simple like this:

server.py (line 89)

`chat = Chat_Server()
 chat.run('', 9005) # adjust host/port`
 
 client.py (line 54)
 
`client = Client()
client.connect('', 9005) # adjust host/port`
