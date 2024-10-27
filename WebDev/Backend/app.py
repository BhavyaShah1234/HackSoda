from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import request
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) #this is the database 
bcrypt = Bcrypt(app) # this is the encryption for the password
login_manager = LoginManager(app) # uses the login manager by flask
login_manager.login_view = 'login' # the view that is going to be used for login



# User Model for the Database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False)

class password(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)

class address(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(60), nullable=False)

class img(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(60), nullable=False) # this is going to be a database that contains images 


# This is the function that is going to be used to load the user BY EMAIL ID
@login_manager.user_loader
def load_user(email_id):
    return User.query.get(int(email_id)) # get the user by the email id 


# if email exists and if password exists then login the user
@app.route("/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated: # if the user already loggin in then redirect to home page
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email') # gets the email from the form 
        password = request.form.get('password') # gets the password from the form 
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # encrypts the password
        user = User(email=email, password=hashed_password, address=address, img=img) # creates a new user
        db.session.add(user) # adds the user to the database
        db.session.commit() # commits the changes to the database 
        flash('Your account has been created!', 'success') 
        return redirect(url_for('login'))
    
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)


