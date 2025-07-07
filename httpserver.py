import os
import socket

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8001

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print('request', request)

    # Get headers of the relevant resource
    headers = request.split('\n')
    print('headers', headers)

    # Parse the request line
    request_type = headers[0].split()[0] # e.g. GET, POST, DELETE, PATCH, PUT
    request_resource = headers[0].split()[1] # e.g. / or /example.html or /file.cpp
    request_protocol = headers[0].split()[2] # e.g. HTTP/1.1

    if request_type == 'GET': # the client wants to GET some resource from the server
        if request_resource == '/':
            request_resource = '/index.html'
        try:
            fin = open('htdocs' + request_resource)
            content = fin.read()
            response = request_protocol + ' 200 OK\n\n' + content
            fin.close()
        except FileNotFoundError:
            response = request_protocol + ' 404 NOT FOUND\n\nFile Not Found'

    # Send HTTP response
    print('response', response)
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
