from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response(
        '<h1>Hello from Pyramid</h1>',
        content_type='text/html'
    )

config = Configurator()
config.add_route('hello', '/hello')
config.add_view(hello_world, route_name='hello')
app = config.make_wsgi_app()