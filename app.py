from flask import Flask 

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.app_context().push()

    return app

app = create_app()

from application.controllers import *

if __name__ == "__main__":
    app.run()

