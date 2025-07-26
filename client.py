import socket

# create the socket on the client side, to pair with the server's socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('localhost', 8888))

# send a message to the server and receive a response
# Note: The server must be running and listening on the specified port
client_sock.sendall(b'test message')
data = client_sock.recv(1024)
print("data", data.decode())

print("client_sock.getsockname()", client_sock.getsockname())