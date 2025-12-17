import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
import re
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'todolist.db')}"
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
db = SQLAlchemy(app)

bootstrap = Bootstrap5(app)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

UPPERCASE_ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_ABC = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[];:,.<>?/|~`"

URGENCY_ORDER = {
    "immediate": 1,
    "timely": 2,
    "flexible": 3
}


class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='lists')

    task_urgency = db.Column(db.String(100), nullable=False, default="flexible")

    created_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)

    items = db.relationship('ToDoItem', back_populates='list', lazy="select", cascade="all, delete")


class ToDoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('to_do_list.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    list = db.relationship('ToDoList', back_populates='items')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    lists = db.relationship('ToDoList', back_populates='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name.title()}>"


with app.app_context():
    db.create_all()
    # Sample data
    if not User.query.first():
        db.session.add(User(first_name="Super", last_name="Admin", email="admin@gmail.com", password=generate_password_hash("11111")))
        db.session.commit()

@app.route('/')
def home():
    today = date.today()
    return render_template('home.html', today=today)

@app.route('/about')
def about():
    today = date.today()
    return render_template('about.html', today=today)

@app.route('/member/<int:user_id>', methods=['GET', 'POST'])
def member(user_id):
    today = date.today()
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You do not have access to this page.", "danger")
        return redirect(url_for('home'))

    user = User.query.get_or_404(user_id)
    user_id = session['user_id']
    todo_list = ToDoList.query.filter_by(user_id=user_id)
    items = ToDoItem.query.filter_by(user_id=user_id).all()
    return render_template('member.html', today=today, user=user, user_id=user_id, todo_list=todo_list, items=items)

@app.route('/new_todo', methods=['GET', 'POST'])
def new_todo():
    today = date.today()

    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get("title") or "Untitled List"

        urgency = request.form.get('features')
        if not urgency:
            urgency = "flexible"
            flash("No Task Urgency selected. 'Flexible' has been set as default.", "warning")

        items = request.form.getlist("items")  # All tasks submitted via hidden inputs

        raw_due_date = request.form.get("due_date")
        if raw_due_date:
            # User selected a date
            due_date = date.fromisoformat(raw_due_date)
        else:
            # User left it blank → default to 2 weeks from today
            due_date = date.today() + timedelta(weeks=2)
            flash("No due date selected. A default date two weeks from today has been set.", "warning")


        # Create new ToDoList
        todo_list = ToDoList(
            title=title,
            task_urgency=urgency,
            user_id=session['user_id'],
            due_date=due_date
        )
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

    return render_template('new_todo.html', user_id=session['user_id'], today=today)

@app.route('/<int:user_id>/old_todo/<int:todo_id>', methods=['GET', 'POST'])
def old_todo(user_id, todo_id):
    today = date.today()
    todo_list = ToDoList.query.get_or_404(todo_id)
    if 'user_id' not in session or todo_list.user_id != session['user_id']:
        flash("You do not have access to this to-do list.", "danger")
        return redirect(url_for('home'))
    else:

        if request.method == 'POST':

            new_title = request.form.get("title")
            if new_title and new_title.strip():
                todo_list.title = new_title.strip()

            new_urgency = request.form.get("features")
            if new_urgency and new_urgency != todo_list.task_urgency:
                todo_list.task_urgency = new_urgency

            raw_due_date = request.form.get("due_date")
            if raw_due_date:
                new_due_date = date.fromisoformat(raw_due_date)

                if new_due_date != todo_list.due_date:
                    todo_list.due_date = new_due_date

            # UPDATE EXISTING ITEMS
            items = ToDoItem.query.filter_by(list_id=todo_id).all()

            for item in items:
                item_text = request.form.get(f"item_{item.id}_text")
                item_completed = request.form.get(f"item_{item.id}_completed") == "on"

                if item_text is not None:     # prevents NULL updates
                    item.text = item_text

                item.completed = item_completed

            # ADD NEW ITEMS
            new_items = request.form.getlist("items")

            for text in new_items:
                if text.strip():
                    db.session.add(ToDoItem(
                        text=text,
                        task_urgency=todo_list.task_urgency,
                        due_date=todo_list.due_date,
                        list_id=todo_list.id,
                        user_id=session['user_id']
                    ))

            db.session.commit()
            flash("To-do list updated!", "success")
            return redirect(url_for('old_todo', user_id=user_id, todo_id=todo_id))


        items = ToDoItem.query.filter_by(list_id=todo_id).all()
        return render_template('old_todo.html', user_id=session['user_id'], todo_list=todo_list, items=items, today=today)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        return "Unauthorized", 401

    item = ToDoItem.query.get_or_404(item_id)
    if item.user_id != session['user_id']:
        return "Unauthorized", 401

    db.session.delete(item)
    db.session.commit()
    return "OK", 200

@app.route('/delete_list/<int:list_id>', methods=['POST'])
def delete_list(list_id):
    if 'user_id' not in session:
        return "Unauthorized", 401

    todo_list = ToDoList.query.get_or_404(list_id)

    if todo_list.user_id != session['user_id']:
        return "Unauthorized", 401

    db.session.delete(todo_list)
    db.session.commit()
    return "OK", 200

@app.context_processor
def inject_user_todos():
    if 'user_id' in session:
        todos = ToDoList.query.filter_by(user_id=session['user_id']).all()
        sorted_old_todos = sorted(todos, key=lambda t: URGENCY_ORDER.get(t.task_urgency, 99))
        return dict(old_todos=sorted_old_todos)
    return dict(old_todos=[])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.permanent = False  # important: expires on browser close
            # Login successful
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['user_id'] = user.id
            return redirect(url_for('new_todo', user_id=user.id))
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
            return redirect(url_for('signup', tab='signup'))

        if len(password) <= 8:
            flash("Password needs to be more than 8 characters including at least one of these: alphabets lowercase and upper case, digit and symbol.", "danger")
            return redirect(url_for('signup', tab='signup'))

        has_upper = any(ch in UPPERCASE_ABC for ch in password)
        has_lower = any(ch in UPPERCASE_ABC for ch in password)
        has_digit = any(ch in UPPERCASE_ABC for ch in password)
        has_symbol = any(ch in UPPERCASE_ABC for ch in password)

        if not (has_upper and has_lower and has_digit and has_symbol):
            flash("Password must include at least one uppercase letter, one lowercase letter, one number, and one symbol.", "danger")
            return redirect(url_for('signup', tab='signup'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('signup', tab='signup'))

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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.before_request
def make_session_non_permanent():
    session.permanent = False


if __name__ == '__main__':
    app.run(debug=True)