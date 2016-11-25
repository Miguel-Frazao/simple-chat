# simple-chat done in python 3

This is a simple socket based chat made in python 3.5.2

`server_short.py`: is exactly the same as `server_extended.py` but without the server side prints. The prints are just to trace what's happening and help you understand what's happening.

I could do this with `sys.argv` arguments, but you can adjust host/port on the code, i thought it would be more simple like this:

server.py (line 89)

`chat = Chat_Server()`<br>
`chat.run('', 9005) # adjust host/port`
 
 client.py (line 54)
 
`client = Client()`<br>
`client.connect('', 9005) # adjust host/port`
