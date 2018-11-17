from flask import Flask, render_template, request, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, validators, SubmitField 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'keepitreal'
boostrap = Bootstrap(app)

class Userform(Form):
    firstname = StringField('First Name')
    surname = StringField('Surname')
    submitme = SubmitField('Register Me')

@app.route('/', methods=['GET', 'POST'])
def main():
    userform = Userform()
    if userform.validate_on_submit():
        print(userform.firstname.data, userform.surname.data)
    return render_template('base.html', userform=userform)

if __name__ == "__main__":
    app.run(debug=True)