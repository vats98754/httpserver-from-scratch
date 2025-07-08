from flask import Flask
from flask import Response

flask_app = Flask(__name__)

@flask_app.route('/hello')
def hello_world():
    return Response(
        '<h1>Hello from Flask</h1>',
        mimetype='text/html'
    )

app = flask_app.wsgi_app