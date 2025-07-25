routes = {}

def route(path, methods=['GET']):
    def decorator(func):
        for method in methods:
            routes[(method, path)] = func
        return func
    return decorator

def app(env, start_response):
    """Barebones WSGI application wherein we create our own Web framework"""
    status = '200 OK'
    response_body = b'Hello world from WSGI Web framework! This is not Flask or Pyramid!'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]

@route('/')
def home(env, start_response):
    status = '200 OK'
    response_body = b'Welcome to home page with route /'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]

@route('/api/users', methods=['GET', 'POST'])
def users_api(env, start_response):
    method = env['REQUEST_METHOD']
    status = '200 OK'

    if method == 'GET':
        response_body = b'{"users": ["anvay", "vats"]}'
        content_type = 'application/json'
    else: # POST request
        response_body = b'{"message": "User created sucessfully!"]}'
        content_type = 'application/json'
    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_body)
    return [response_body]
