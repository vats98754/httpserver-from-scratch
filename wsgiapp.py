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
