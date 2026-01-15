# Import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from models import db, User, URL
import validators
import random
import string
app = Flask(__name__)
app.secret_key = "secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advanced_urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Create ROUTES 

@app.route("/")
def home():
    return "Advanced URL Shortener App Started"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if len(username) < 5 or len(username) > 9:
            error = "Username must be between 5 to 9 characters long"
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                error = "This username already exists"
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))

    return render_template("signup.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            error = "Invalid username or password"
        else:
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    error = None
    short_url = None

    if request.method == "POST":
        original_url = request.form.get("url")

        if not validators.url(original_url):
            error = "Please enter a valid URL"
        else:
            short_code = generate_short_code()

            new_url = URL(
                original_url=original_url,
                short_code=short_code,
                user_id=current_user.id
            )

            db.session.add(new_url)
            db.session.commit()

            short_url = request.host_url + short_code

    user_urls = URL.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard.html",
        error=error,
        short_url=short_url,
        urls=user_urls
    )
@app.route("/<short_code>")
def redirect_short_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        return redirect(url_entry.original_url)
    else:
        return "Invalid short URL", 404

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# run the application
if __name__ == "__main__":
    app.run(debug=True)
