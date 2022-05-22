from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# this import must be after the app instantiation & config
from . import routes