"""from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from flask_mail import Mail
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "images"
)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


mail = Mail()

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")



mail.init_app(app)

from routes import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
"""
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from flask_mail import Mail
import os

app = Flask(__name__)

app.config.from_object(Config)

# ---------------------------------
# Upload folder
# ---------------------------------
app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "images"
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ---------------------------------
# Database
# ---------------------------------
db.init_app(app)

# ---------------------------------
# Login Manager
# ---------------------------------
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


# ---------------------------------
# Flask-Mail
# ---------------------------------
app.config["MAIL_SERVER"] = os.getenv(
    "MAIL_SERVER",
    "smtp.gmail.com"
)

app.config["MAIL_PORT"] = int(
    os.getenv("MAIL_PORT", "587")
)

app.config["MAIL_USE_TLS"] = (
    os.getenv("MAIL_USE_TLS", "True").lower() == "true"
)

app.config["MAIL_USE_SSL"] = False

app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")


mail = Mail(app)


# ---------------------------------
# Routes
# ---------------------------------
from routes import *


# ---------------------------------
# Create database tables
# ---------------------------------
with app.app_context():
    db.create_all()


# ---------------------------------
# Local development
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)

