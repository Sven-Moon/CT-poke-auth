from flask import render_template
from app import app

@app.route('/')
def home():
 
    return render_template('home.html')

@app.route('/explorer/display')
def display():
 
    return render_template('display.html')

@app.route('/explorer')
def explorer():
 
    return render_template('explorer.html')