from flask import Flask 
from application.database import db
from application.resources import api, TransApi

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///lmsdata.sqlite3"
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()

    return app

app = create_app()

from application.controllers import *
# from application.models import *

# with app.app_context():
#     # add your code here

if __name__ == "__main__":
    app.run()

