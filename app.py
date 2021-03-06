import sys
sys.path.append('/home/PyJan/myproject/Bootstrap_base')
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import length, email
import datetime
from flask_migrate import Migrate
from flask_script import Manager, Shell
from werkzeug import secure_filename
import os
from flask_mail import Mail, Message
from config.config import USE_MAIL
from logging import FileHandler, WARNING

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuckoffyouhackers112'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sammy:sammy@localhost:5432/sammy'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

bootstrap = Bootstrap(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
mail = Mail(app)

if app.debug == False:
    file_handler = FileHandler('errors_file.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    orders = db.relationship('Orders', backref='user')

    def __repr__(self):
        return '<user {0}: id={1}, email={2}, password={3}>'.format(
            self.username,
            self.id,
            self.email,
            self.password
        )

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    itemid = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    volume = db.Column(db.Integer)
    ordered = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)
    delivered = db.Column(db.Boolean)
    orderdate = db.Column(db.TIMESTAMP)
    paydate = db.Column(db.TIMESTAMP)
    deliverydate = db.Column(db.TIMESTAMP)


    def __repr__(self):
        return '<order number {0}: userid={1}, itemid={2}, volume={3}>'.format(
            self.id,
            self.userid,
            self.itemid,
            self.volume
        )

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    orders = db.relationship('Orders', backref='item')

    def __repr__(self):
        return '<item {0}: id={1}>'.format(self.name, self.id)

class ItemsDesc(db.Model):
    __tablename__ = 'itemsdesc'
    id = db.Column(db.Integer, primary_key=True)
    itemid = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String)
    imgref = db.Column(db.String)

    item = db.relationship('Items', backref=db.backref('itemdesc', uselist=False))

class Prices(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    itemid = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    price = db.Column(db.Integer)
    validfrom = db.Column(db.TIMESTAMP)
    validto = db.Column(db.TIMESTAMP)

    item = db.relationship('Items', backref='pricetags')

class LoginForm(FlaskForm):
    username = StringField('User name: ', validators=[length(min=3, max=30)])
    password = PasswordField('Password: ', validators=[length(min=5, max=30)])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField('User name: ', validators=[length(min=3, max=30)])
    email = StringField('Email: ', validators=[email(message='Not valid email address')])
    password = PasswordField('Password: ', validators=[length(min=5, max=30)])
    submit = SubmitField('Sign up')

class InsertItem(FlaskForm):
    internalname = StringField('Internal name: ', validators=[length(min=3)])
    pagename = StringField('Page name: ', validators=[length(min=3)])
    description = TextAreaField('Description: ')
    price = StringField('Price: ')
    picture = FileField('Load picture', validators=[FileRequired('No picture provided')])
    submit = SubmitField('Save')

@loginmanager.user_loader
def loaduser(userid):
    return User.query.get(int(userid))

@app.route('/')
def main():
    items = ItemsDesc.query.all()
    return render_template('vlab.html',items=items)

@app.route('/selection/<product>')
def selection(product):
    item = ItemsDesc.query.get(int(product))
    price = Prices.query.filter_by(itemid=item.id).first()
    return render_template('product.html', item=item, price=price, 
                            items = ItemsDesc.query.all())

@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
    if request.args.get('productid'):
        chosen_product = Items.query.get(int(request.args.get('productid')))
        user = User.query.filter_by(id=current_user.id).first()
        issued_order = Orders(item=chosen_product, user=user, volume=1)
        db.session.add(issued_order)
        db.session.commit()
    if request.args.get('deletion'):
        product_for_removal = Orders.query.get(int(request.args.get('deletion')))
        db.session.delete(product_for_removal)
        db.session.commit()
    basket = Orders.query.filter(
        Orders.userid==current_user.id,
        db.or_(Orders.ordered.is_(None),
        Orders.ordered.is_(False))).all()
    return render_template('basket.html', basket=basket, totalprice=totalprice(basket), 
        items = ItemsDesc.query.all())

def totalprice(basket):
    totalprice = 0
    for b in basket:
        totalprice += b.item.pricetags[0].price
    return totalprice

@app.route('/myorder', methods=['GET', 'POST'])
def myorder():
    myorder = Orders.query.filter(
        Orders.userid==current_user.id,
        db.or_(Orders.ordered.is_(None),
        Orders.ordered.is_(False))).all()
    for item in myorder:
        item.ordered = True
        item.orderdate = datetime.datetime.now()
    db.session.commit()
    user = User.query.get(current_user.id)
    greetings = user.username
    if USE_MAIL:
        sendmail(user.email, myorder=myorder, totalprice=totalprice(myorder),
                                            greetings=greetings)
    return render_template('myorder.html', myorder=myorder, 
        totalprice=totalprice(myorder), items = ItemsDesc.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        if loginform.username.data == 'admin' and loginform.password.data == 'vikinka':
            user = User(username='admin', password='vikinka', email='vikinka@seznam.cz')
            return redirect(url_for('adminpage')) 
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

@app.route('/showbase')
def showbase():
    signupform = SignupForm()
    return render_template('base.html', userform=signupform)

@app.route('/adminpage')
def adminpage():
    return render_template('adminpage.html')

@app.route('/payments', methods=['GET','POST'])
def payments():
    if request.method == 'POST':
        to_update_paid = db.session.query(Orders).filter(
            Orders.id.in_(request.form.getlist('paid'))).all()
        for order in to_update_paid:
            order.paid = True
            order.paydate = datetime.datetime.now()
        db.session.commit()
        to_update_delivered = db.session.query(Orders).filter(
            Orders.id.in_(request.form.getlist('delivered'))).all()
        for order in to_update_delivered:
            order.delivered = True
            order.deliverydate = datetime.datetime.now()
        db.session.commit()
    orders = Orders.query.filter(db.or_(~Orders.paid.is_(True),
                                ~Orders.delivered.is_(True))).all()
    return render_template('payments.html', orders=orders)

@app.route('/insertitem', methods=['GET','POST'])
def insertitem():
    print('in insert item')
    insertitem = InsertItem()
    print(insertitem)
    if insertitem.validate_on_submit():
        filename = secure_filename(insertitem.picture.data.filename)
        insertitem.picture.data.save('static/' + filename)  
        item = Items(name=insertitem.internalname.data)
        itemdesc = ItemsDesc(item=item, name=insertitem.pagename.data, 
                            desc=insertitem.description.data, imgref=filename)
        price = Prices(item=item, price=int(insertitem.price.data))
        db.session.add(item)
        db.session.add(itemdesc)
        db.session.add(price)
        db.session.commit()
        return redirect(url_for('insertitem'))
    return render_template('insertitem.html', form=insertitem)

@app.route('/deleteitem', methods=['GET','POST'])
def deleteitem():
    if 'deletion' in request.args:
        itemdesc = ItemsDesc.query.get(request.args['deletion'])
        item = Items.query.get(itemdesc.item.id)
        price = Prices.query.get(itemdesc.item.id)
        db.session.delete(price)
        db.session.commit()
        db.session.delete(itemdesc)
        db.session.commit()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('deleteitem'))
    itemdescs = ItemsDesc.query.all()
    return render_template('deleteitem.html', itemdescs=itemdescs)

def sendmail(to, myorder, totalprice, greetings):
    msg = Message("Viki's lab - order confimation", sender='pyjan3@gmail.com',
                    recipients=[to])
    msg.body = 'text body'
    msg.html = render_template('emailtemplate.html', myorder=myorder, 
                                totalprice=totalprice, greetings=greetings)
    mail.send(msg)

def make_shell_context():
    return dict(app=app, db=db, User=User, Orders=Orders, Items=Items, 
                ItemsDesc=ItemsDesc)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    #app.run(debug=True)
    manager.run()