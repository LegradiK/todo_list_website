import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
import re
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'todolist.db')}"
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
db = SQLAlchemy(app)

bootstrap = Bootstrap5(app)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    items = db.relationship('ToDoItem', backref='list', lazy=True, cascade="all, delete")


class ToDoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    lists = db.relationship('ToDoList', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name.title()}>"


with app.app_context():
    db.create_all()
    # Sample data
    if not User.query.first():
        db.session.add(User(first_name="Alice", last_name="Johnson", email="alice@example.com", password=generate_password_hash("11111")))
        db.session.add(User(first_name="Bob", last_name="Smith", email="bob@example.com", password=generate_password_hash("22222")))
        db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/new_todo', methods=['GET', 'POST'])
def new_todo():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get("title") or "Untitled List"
        items = request.form.getlist("items")  # All tasks submitted via hidden inputs

        # Create new ToDoList
        todo_list = ToDoList(title=title, user_id=session['user_id'])
        db.session.add(todo_list)
        db.session.flush()  # Get todo_list.id without committing

        # Add tasks to ToDoItem table
        for item_text in items:
            todo_item = ToDoItem(
                text=item_text,
                list_id=todo_list.id,
                user_id=session['user_id']
            )
            db.session.add(todo_item)

        db.session.commit()
        flash("New to-do list created!", "success")
        return redirect(url_for('new_todo'))

    return render_template('new_todo.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Login successful
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['user_id'] = user.id
            return redirect(url_for('new_todo'))
        else:
            # Login failed
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login_signup.html')

@app.route('/signup' , methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if email is valid
        if not re.match(EMAIL_REGEX, email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('signup'))

        # Optional: check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('login_signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)