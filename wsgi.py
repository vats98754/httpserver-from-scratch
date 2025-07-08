import io
import sys
import socket

class WSGIServer(object):
    # Default address family for IPv4
    address_family = socket.AF_INET
    # Default socket type for TCP
    socket_type = socket.SOCK_STREAM
    # The maximum number of queued connections that can be waiting to be accepted
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a client socket object with the specified address family and socket type
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow the client socket with same address to be reused immediately after the server is stopped
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the client socket to the specified server address
        listen_socket.bind(server_address)
        # Start listening for incoming connections
        listen_socket.listen(self.request_queue_size)
        # Get server host and port name
        host, port = listen_socket.getsockname()[:2]
        # Retrieve the fully qualified domain name of the server host and set server port
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers = []
    
    def set_app(self, application):
        # Set the WSGI application to be served
        self.application = application
    
    def serve_forever(self):
        listen_socket = self.listen_socket
        # Start an infinite loop to accept incoming connections
        while True:
            # Accept a new client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection
            self.handle_one_request()

    def handle_one_request(self):
        request = self.client_connection.recv(1024)
        self.request_data = request_data = request.decode()
        # Print request data to the console for debugging
        print(f'<-- {line} -->\n' for line in request_data.splitlines())
        # Parse the request data to extract method, path, and headers
        self.parse_request(request_data)

        # Construct the environment dictionary using request data
        env = self.get_environ()

        # Call the WSGI application callable and get the result
        # The result will become our HTTP response body
        result = self.application(env, self.start_response)

        # Construct a response and send back to client
        self.finish_response(result)
    
    def parse_request(self, request_data):
        request_line = request_data.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Extract the request method, path, and HTTP version from the request line
        (self.request_method, self.path,  self.request_version) = request_line.split()

    def get_environ(self):
        # Create the environment dictionary for WSGI
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values

        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False

        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 8 Jul 2025 12:00:00 GMT'),
            ('Server', 'WSGIServer/0.1'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        self.headers_set = [status, server_headers + response_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. For simplicity's sake we'll ignore that detail for now.
        # return self.finish_response

    def final_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            # Add server headers to the response
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            # Add the result body to the response
            for byte_data in result:
                response += byte_data.decode()

            # Print response data
            print(f'<-- {line} -->\n' for line in response.splitlines())
            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            # Close the client connection after sending the response
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = ('localhost', 8888)

def make_server(server_address, application):
    # Create a WSGIServer instance with the specified server address
    server = WSGIServer(server_address)
    # Set the WSGI application to be served
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':', 1)
    module = __import__(module)
    application = getattr(module, application)
    # Create a WSGIServer instance with the specified server address
    httpd = make_server(SERVER_ADDRESS, application)
    # Start serving requests indefinitely
    print(f'WSGIServer: Serving HTTP on {HOST}:{PORT}...\n')
    httpd.serve_forever()
