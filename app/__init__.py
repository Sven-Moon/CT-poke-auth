from flask import Flask
from config import Config
from .forms import SearchForm
from .auth.routes import auth
from .models import db, login
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app,db)
login.init_app(app)
login.login_view = 'auth.login'
login.login_message = 'Go login'
login.login_message_category = 'danger'
# this import must be after the app instantiation & config
from . import routes