from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import length, email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuckoffyouhackers112'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logins.db'

bootstrap = Bootstrap(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    itemid = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    paid = db.Column(db.Boolean)
    orderdate = db.Column(db.DateTime)

class LoginForm(FlaskForm):
    username = StringField('User name: ', validators=[length(min=3, max=30)])
    password = PasswordField('Password: ', validators=[length(min=5, max=30)])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField('User name: ', validators=[length(min=3, max=30)])
    email = StringField('Email: ', validators=[email(message='Not valid email address')])
    password = PasswordField('Password: ', validators=[length(min=5, max=30)])
    submit = SubmitField('Sign up')

@loginmanager.user_loader
def loaduser(userid):
    return User.query.get(int(userid))

@app.route('/')
def main():
    return render_template('vlab.html')

@app.route('/selection/<product>')
def selection(product):
    return render_template('products/'+product+'.html')

@app.route('/basket')
def basket():
    print(current_user.username)
    basket = Orders.query.filter_by(userid=current_user.id).all()
    #print(basket.itemid, basket.paid)
    return render_template('basket.html', basket=basket)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is None:
            loginform.username.errors.append('Wrong user name')
        else:
            if user.password == loginform.password.data:
                login_user(user)
                return redirect(url_for('main'))
            else:
                loginform.password.errors.append('Wrong password')        
    return render_template('login.html', loginform=loginform)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignupForm()
    if signupform.validate_on_submit():
        user = User.query.filter_by(username=signupform.username.data).first()
        if user is None:
            user = User(username=signupform.username.data,
                        email=signupform.email.data,
                        password=signupform.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
        else:
            signupform.username.errors.append('This user already exists')
    return render_template('signup.html', signupform=signupform)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/loggedin')
@login_required
def loggedin():
    return 'current user is {0}'.format(current_user.username)

if __name__ == "__main__":
    app.run(debug=True)