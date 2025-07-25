import re
from urllib.parse import parse_qs

routes = {}

def route(path, methods=['GET']):
    def decorator(func):
        for method in methods:
            routes[(method, path)] = func
        return func
    return decorator

# for routes with URL parameters
def route_with_params(pattern, methods=['GET']):
    def decorator(func):
        compiled_pattern = re.compile(pattern)
        for method in methods:
            routes[(method, pattern)] = (func, compiled_pattern)
        return func
    return decorator

def get_query_params(env):
    query_string = env.get('QUERY_STRING', '')
    return parse_qs(query_string)

def get_request_body(env):
    content_length = int(env.get('CONTENT_LENGTH', 0))
    if content_length:
        return env['wsgi.input'].read(content_length)
    return b''

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

@route('/about')
def about(env, start_response):
    status = '200 OK'
    response_body = b'This is the about page'
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

@route_with_params(r'/user/(\d+)')
def user_detail(env, start_response, user_id):
    # Handle /user/123
    pass