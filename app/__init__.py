import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app.users.views import users_blueprint
app.register_blueprint(users_blueprint) 
from app.api.views import api_blueprint
app.register_blueprint(api_blueprint)
from app.home.views import home_blueprint
app.register_blueprint(home_blueprint)

from app.models import Users, Place, Menu

login_manager.login_view = "users.login"
login_manager.login_message = u'You need to login first!'
login_manager.login_message_category = 'info'


# loads users info from db and stores it in a session
@login_manager.user_loader 
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).first()