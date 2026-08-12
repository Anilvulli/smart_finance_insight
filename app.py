from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import routes
app.register_blueprint(routes)

with app.app_context():
    db.create_all()



mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
