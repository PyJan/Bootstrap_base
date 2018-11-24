from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('basket.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username='Jan').first()
        login_user(user)
        return redirect(url_for('loggedin'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logged out'

@app.route('/loggedin')
@login_required
def loggedin():
    return 'current user is {0}'.format(current_user.username)

if __name__ == "__main__":
    app.run(debug=True)