import os
import socket
import urllib.parse
import json

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
    header_dict = {}
    headers, body = request.split('\r\n', 1)
    for line in headers.split('\r\n')[1:]:  # Skip first line (request line)
        if ': ' in line:
            key, value = line.split(': ', 1)
            header_dict[key] = value

    print('header_dict', header_dict)

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

    elif request_type == 'POST': # the client wants to POST some data to the server
        print('POST request body:', body)

        # Handle form data, if content type is application/x-www-form-urlencoded
        if header_dict.get('content-type', '').startswith('application/x-www-form-urlencoded'):
            form_data = body.split('&')
            form_dict = {}
            for item in form_data:
                key, value = item.split('=', 1)
                value = value.replace('+', ' ')
                value = urllib.parse.unquote(value)
                form_dict[key] = value
            print('Form data:', form_dict)

        # Handle JSON data
        elif header_dict.get('content-type', '').startswith('application/json'):
            # For simplicity, we assume the body is a simple string
            # In a real application, you would parse JSON here
            try:
                json_data = json.loads(body)
                print('JSON data:', json_data)
            except json.JSONDecodeError:
                print('Invalid JSON data received')
                response = request_protocol + ' 400 BAD REQUEST\n\nInvalid JSON data'

        response = request_protocol + ' 200 OK\n\nPOST request processed successfully'

    # Send HTTP response
    print('response', response)
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
