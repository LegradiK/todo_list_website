import os
from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/new_todo')
def new_todo():
    return render_template('new_todo.html')

if __name__ == '__main__':
    app.run(debug=True)