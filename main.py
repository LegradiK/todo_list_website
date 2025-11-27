import os
from flask import Flask, render_template, session
from bootstrap_flask import Bootstrap5


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

@app.route('/')
def home():
    return render_template('home.html')