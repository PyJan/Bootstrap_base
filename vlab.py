from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def main():
    return render_template('vlab.html')

@app.route('/selection/<product>')
def selection(product):
    return render_template('products/'+product+'.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')

if __name__ == "__main__":
    app.run(debug=True)