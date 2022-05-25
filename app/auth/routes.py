from tabnanny import check
from flask import Blueprint, redirect, render_template, request, flash, url_for
from app.auth.forms import LoginForm, RegisterForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user,current_user


auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates' )

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            print(user)
            # check if username/pw correct
            print(user.password, form.username.data)
            if user and check_password_hash(user.password, form.password.data):
            # if so, log in & advance next_page or home, w/ msg
                login_user(user)
                flash('You logged in. Great.', 'success')
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for('home'))
            # if fail, redirect to login with msg
            flash('You did something wrong. Not me. You.', 'danger')    
    return render_template('login.html',form=form)

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    # check to make sure not already registered
    if request.method == 'POST':
        if form.validate_on_submit():
            user_name = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(email=form.email.data).first()
            print(user_name)
            print(email)
            if not (user_name or email):
                user = User(form.username.data,form.email.data,form.password.data)
                try:
                    db.session.add(user)
                    db.session.commit()
                except:
                    flash('There was an unknown error when trying to register you', 'danger')
                    return redirect(url_for('auth.register'))                    
                login_user(user)
                flash(f"Welcome to your Pokehome. We\'ll call you {current_user.username}. We don't even care about your real name.")
                return redirect(url_for('home'))  
            elif user_name:
                flash('That username has been taken. Be more creative.', 'warning')
            else:
                flash('That email is in use. Maybe you made an account when in a drunken stupor?', 'warning')
            return redirect(url_for('auth.register'))                              
    return render_template('register.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bye!', 'info')
    return redirect(url_for('home'))
