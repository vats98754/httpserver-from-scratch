import os
import socket
import urllib.parse
import json

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8001

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set socket options to reuse address
# This allows the server to restart without waiting for the socket to be released
# This is useful during development to avoid "Address already in use" errors
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind socket to host and port
# This binds the server to all available interfaces (0.0.0.0)
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Start listening for incoming connections
# The argument 1 means the server can queue up to 1 connection request
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    # The accept() method blocks until a client connects
    # It returns a new socket object representing the connection and the address of the client
        # - client_connection is the new socket object for the connection
        # - client_address is the address of the client that connected
    client_connection, client_address = server_socket.accept()

    # Get the client request data, with maximum buffer size of 1024 bytes
    # If the request is larger than 1024 bytes, it will be truncated
    request_data = client_connection.recv(1024)
        
    # Decode the request data from bytes to string
    request = request_data.decode()
    print('request', request)

    # Get headers of the relevant resource
    header_dict = {}
    body = ""
    if '\r\n\r\n' in request:
        headers, body = request.split('\r\n\r\n', 1)
    else:
        headers = request

    header_lines = headers.split('\r\n')
    request_line = header_lines[0]  # First line is the request line
    for line in header_lines[1:]:  # Skip first line (request line)
        if ': ' in line:
            key, value = line.split(': ', 1)
            header_dict[key] = value

    print('header_dict', header_dict)

    # Parse the request line
    request_type = request_line.split()[0] # e.g. GET, POST, DELETE, PATCH, PUT
    request_resource = request_line.split()[1] # e.g. / or /example.html or /file.cpp
    request_protocol = request_line.split()[2] # e.g. HTTP/1.1

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

    elif request_type == 'POST': # the client wants to POST some data to the server
        print('POST request body:', body)
        
        if request_resource == '/submit-form':
            # Handle form data, if content type is application/x-www-form-urlencoded
            if header_dict.get('Content-Type', '').startswith('application/x-www-form-urlencoded'):
                form_data = body.split('&')
                form_dict = {}
                for item in form_data:
                    key, value = item.split('=', 1)
                    value = value.replace('+', ' ')
                    value = urllib.parse.unquote(value)
                    form_dict[key] = value
                print('Form data:', form_dict)
                response = request_protocol + ' 200 OK\n\nPOST request processed successfully'
            else:
                response = request_protocol + ' 400 BAD REQUEST\n\nExpected form data'

        elif request_resource == '/submit-json':
            # Handle JSON data
            if header_dict.get('Content-Type', '').startswith('application/json'):
                # For simplicity, we assume the body is a simple string
                # In a real application, you would parse JSON here
                try:
                    json_data = json.loads(body)
                    print('JSON data:', json_data)
                    # Download or process the JSON data as needed
                    with open('data.json', 'w') as json_file:
                        json.dump(json_data, json_file)

                    response = request_protocol + ' 200 OK\n\nPOST request processed successfully with JSON data'
                except json.JSONDecodeError:
                    print('Invalid JSON data received')
                    response = request_protocol + ' 400 BAD REQUEST\n\nInvalid JSON'
            else:
                response = request_protocol + ' 400 BAD REQUEST\n\nExpected JSON data'

        else:
            response = request_protocol + ' 404 NOT FOUND\n\nEndpoint not found'

    # Send HTTP response
    print('response', response)
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
