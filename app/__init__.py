from flask import Flask
from config import Config
from .forms import SearchForm
from .auth.routes import auth


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)
# this import must be after the app instantiation & config
from . import routes