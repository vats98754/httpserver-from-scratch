import os
import socket
import time

SERVER_ADDRESS = ('localhost', 8888)
REQUEST_QUEUE_SIZE = 2

def handle_request(client_socket, client_address):
    request_data = client_socket.recv(1024)
    print(f"Child Process ID: {os.getpid()}\nParent Process ID: {os.getppid()}")
    print(f"received client request_data from {client_address}: {request_data.decode()}")
    # Prepare a simple HTTP response
    http_response = b'HTTP/1.1 200 OK\r\n\r\nServer response'
    # Simulate a processing time for the request
    time.sleep(20)
    client_socket.sendall(http_response)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print(f'Serving HTTP on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]} ...')
    print(f'Parent Process ID: {os.getppid()}\n')

    clients = []
    while True:
        client_socket, client_address = listen_socket.accept()
        print(f'Accepted connection from {client_address}')
        # store the reference otherwise it's garbage collected on the next loop run
        clients.append(client_socket)
        pid = os.fork() # creates new child process by duplicating current process
        # return value and PID of child process is 0
        """
        the sole role of the server parent process now is to accept a new client connection,
        fork a new child process to handle that client request, and loop over to accept
        another client connection, and nothing more. The server parent process does not
        process client requests - its children do.
        """
        if pid == 0: # child
            listen_socket.close() # close child copy
            handle_request(client_socket, client_address)
            client_socket.close()
            os._exit(0) # child exits here
        else: # parent
            # client_socket.close()
            print("client count:", len(clients))

        print(f'Finished handling request from {client_address}')

if __name__ == '__main__':
    serve_forever()