from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def main():
    return render_template('vlab.html')

if __name__ == "__main__":
    app.run(debug=True)