# simple-chat-python3

This is a simple socket based chat made in python 3.5.2

I could do this with `sys.argv` arguments, but you can adjust host/port on the code, i thought it would be more simple like this:

server.py (line 89)

`chat = Chat_Server()`<br>
`chat.run('', 9005) # adjust host/port`
 
 client.py (line 54)
 
`client = Client()`<br>
`client.connect('', 9005) # adjust host/port`

Don't worry, if you find this big you can delete the prints, we don't really need them, and the code will be half size
