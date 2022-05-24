from flask import Blueprint


auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates' )

@auth.route('/login')
def login():
    
    return render_template('login.html')

@auth.route('/register')
def register():
    
    return render_template('register.html')