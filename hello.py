from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    app.logger.debug('/ route called')
    return 'Hello, World!'