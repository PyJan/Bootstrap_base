from flask_mail import Mail, Message
from flask import Flask


app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pyjan3@gmail.com'#os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'svarj4AM'#s.environ.get('MAIL_PASSWORD')

mail = Mail(app)
msg = Message('test subject', sender='pyjan3@gmail.com',
recipients=['jan.svarcbach@gmail.com'])
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
    mail.send(msg)