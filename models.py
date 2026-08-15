from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date)

    gender = db.Column(db.String(20))

    occupation = db.Column(db.String(100))

    monthly_income = db.Column(db.Float)

    city = db.Column(db.String(100))

    address = db.Column(db.Text)

    profile_image = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Expense(db.Model):

    __tablename__ = "expenses"

    expense_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    category = db.Column(db.String(100), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    payment_method = db.Column(db.String(50))

    expense_date = db.Column(db.Date)

    description = db.Column(db.String(250))
class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    source = db.Column(db.String(100), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    income_date = db.Column(db.Date, nullable=False)

    description = db.Column(db.String(255))
class Budget(db.Model):
    __tablename__ = "budget"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category = db.Column(db.String(100), nullable=False)

    budget_amount = db.Column(db.Float, nullable=False)

    month = db.Column(db.String(20), nullable=False)

    year = db.Column(db.Integer, nullable=False)


class Investment(db.Model):
    __tablename__ = "investment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    investment_type = db.Column(db.String(100))
    investment_name = db.Column(db.String(100))
    amount = db.Column(db.Float)
    current_value = db.Column(db.Float)
    investment_date = db.Column(db.Date)
class Goal(db.Model):
    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    goal_name = db.Column(db.String(100))
    target_amount = db.Column(db.Float)
    saved_amount = db.Column(db.Float)
    target_date = db.Column(db.Date)




class Notification(db.Model):

    __tablename__ = "notification"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.String(500),
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    
def create_notification(user_id, title, message,
                        priority="Medium",
                        status="Active"):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        priority=priority,
        status=status,
        created_at=datetime.utcnow()
    )

    db.session.add(notification)


# class Feedback(db.Model):

#     __tablename__ = "feedback"

#     id = db.Column(db.Integer, primary_key=True)

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey("users.id"),   
#         nullable=False
#     )

#     rating = db.Column(db.Integer)

#     subject = db.Column(db.String(100))

#     message = db.Column(db.Text)

#     created_at = db.Column(
#         db.DateTime,
#         default=datetime.utcnow
#     )

#     user = db.relationship(
#         "User",
#         backref="feedbacks"
#     )
