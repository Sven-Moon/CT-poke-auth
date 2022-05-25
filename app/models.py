from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(100),nullable=True)
    username = db.Column(db.String(40), unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self,username,email,password):
        self.id = str(uuid.uuid4)
        self.username = username
        self.email = email
        self.password = password
    
    