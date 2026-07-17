from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)
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

