from flask import Flask, render_template, request, url_for, session
from flask_bootstrap import Bootstrap


app = Flask(__name__)
boostrap = Bootstrap(app)

@app.route('/')
def main():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)