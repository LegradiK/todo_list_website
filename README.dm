# Flask To‑Do List Application

A full‑stack Flask web application that allows users to create, manage, and prioritise to‑do lists with authentication, due dates, urgency levels, and task completion tracking.

---

## Features

### Authentication & Users

* User registration with strong password validation
* Secure login and logout using session management
* Password hashing via Werkzeug
* Email uniqueness enforced

### To‑Do Lists

* Create multiple to‑do lists per user
* Assign urgency levels: **Immediate**, **Timely**, or **Flexible**
* Set custom due dates (defaults to two weeks if omitted)
* Lists automatically sorted by urgency
* Edit list title, urgency, and due date
* Delete entire lists (cascade deletes tasks)

### To‑Do Items

* Add multiple tasks per list
* Mark tasks as completed
* Edit existing tasks
* Dynamically add new tasks to existing lists
* Delete individual tasks via AJAX

### UI & UX

* Bootstrap 5 styling
* Flash messages for user feedback
* Icon‑based interactions for edit/delete/status indicators
* Context processor to display user to‑do lists globally

---

## Tech Stack

* **Backend:** Flask (Python 3)
* **Frontend:** Jinja2, Bootstrap 5
* **Database:** SQLite (SQLAlchemy ORM)
* **Authentication:** Flask sessions + Werkzeug security
* **Icons:** Flaticon (credited below)

---

## Project Structure

```
project/
│── app.py
│── todolist.db
│── templates/
│   ├── home.html
│   ├── about.html
│   ├── login_signup.html
│   ├── member.html
│   ├── new_todo.html
│   └── old_todo.html
│── static/
│   ├── css/
│   ├── js/
│   └── icons/
│── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\\Scripts\\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install flask flask-bootstrap flask-sqlalchemy werkzeug
```

### 4. Set Environment Variables (Optional)

```bash
export FLASK_SECRET_KEY="your-secret-key"
```

### 5. Run the Application

```bash
python app.py
```

The app will be available at:

```
http://127.0.0.1:5000
```

---

## Default Admin User

On first run, the database auto‑creates a sample user:

* **Email:** [admin@gmail.com](mailto:admin@gmail.com)
* **Password:** 11111

(For development purposes only.)

---

## Security Notes

* Passwords are hashed using `generate_password_hash`
* Session expires on browser close (`session.permanent = False`)
* Route‑level authorisation checks prevent unauthorised access

---

## Icon & Asset Credits

All icons used in this project are sourced from **Flaticon** and are credited below with direct links:

* **Delete icon (Recycle bin)**
  [https://www.flaticon.com/free-icons/recycle-bin](https://www.flaticon.com/free-icons/recycle-bin)
  Created by **hqrloveq** – Flaticon

* **Open bin icon**
  [https://www.flaticon.com/free-icons/recycle-bin](https://www.flaticon.com/free-icons/recycle-bin)
  Created by **lakonicon** – Flaticon

* **Closed bin icon**
  [https://www.flaticon.com/free-icons/recycle-bin](https://www.flaticon.com/free-icons/recycle-bin)
  Created by **Hilmy Abiyyu A.** – Flaticon

* **To‑do list icon**
  [https://www.flaticon.com/free-icons/to-do-list](https://www.flaticon.com/free-icons/to-do-list)
  Created by **Freepik** – Flaticon

* **Edit icon**
  [https://www.flaticon.com/free-icons/edit](https://www.flaticon.com/free-icons/edit)
  Created by **Freepik** – Flaticon

* **Red circle icon**
  [https://www.flaticon.com/free-icons/red](https://www.flaticon.com/free-icons/red)
  Created by **hqrloveq** – Flaticon

* **Green circle icon**
  [https://www.flaticon.com/free-icons/rec](https://www.flaticon.com/free-icons/rec)
  Created by **hqrloveq** – Flaticon

* **Orange circle icon**
  [https://www.flaticon.com/free-icons/circle](https://www.flaticon.com/free-icons/circle)
  Created by **Designspace Team** – Flaticon

* **Warning / exclamation mark icon**
  [https://www.flaticon.com/free-icons/exclamation-mark](https://www.flaticon.com/free-icons/exclamation-mark)
  Created by **Creatype** – Flaticon

Template inspiration:

* BBBootstrap – Awesome To‑Do List Template
  [https://bbbootstrap.com/snippets/](https://bbbootstrap.com/snippets/)

---

## Future Improvements

* Pagination for large task lists
* Email verification and password reset
* Task filtering (completed / pending)
* REST API endpoints
* Deployment configuration (Gunicorn + Docker)

---

## Licence

This project is intended for educational and personal use.
