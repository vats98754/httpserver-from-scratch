import socket

SERVER_ADDRESS = ('localhost', 8888)
REQUEST_QUEUE_SIZE = 5

def handle_request(client_socket, client_address):
    request_data = client_socket.recv(1024)
    print(f"received client request_data from {client_address}: {request_data.decode()}")

    http_response = b'HTTP/1.1 200 OK\r\n\r\nServer response'
    client_socket.sendall(http_response)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print(f'Serving HTTP on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]} ...')

    while True:
        client_socket, client_address = listen_socket.accept()
        print(f'Accepted connection from {client_address}')
        handle_request(client_socket, client_address)
        print(f'Finished handling request from {client_address}')
        client_socket.close()

if __name__ == '__main__':
    serve_forever()