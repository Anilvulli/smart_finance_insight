from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField, DateField, SelectField,DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):

    fullname = StringField("Full Name", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")



class ExpenseForm(FlaskForm):

    category = SelectField(
        "Category",
        choices=[
            ("Food","Food"),
            ("Travel","Travel"),
            ("Shopping","Shopping"),
            ("Bills","Bills"),
            ("Medical","Medical"),
            ("Education","Education"),
            ("Other","Other")
        ]
    )

    amount = FloatField(
        "Amount",
        validators=[DataRequired()]
    )

    payment_method = SelectField(
        "Payment Method",
        choices=[
            ("Cash","Cash"),
            ("UPI","UPI"),
            ("Card","Card"),
            ("Net Banking","Net Banking")
        ]
    )

    expense_date = DateField(
        "Expense Date",
        validators=[DataRequired()]
    )

    description = StringField("Description")

    submit = SubmitField("Save Expense")
from wtforms import DateField, DecimalField, TextAreaField

class IncomeForm(FlaskForm):

    source = StringField(
        "Income Source",
        validators=[DataRequired()]
    )

    amount = DecimalField(
        "Amount",
        validators=[DataRequired()]
    )

    income_date = DateField(
        "Date",
        validators=[DataRequired()]
    )

    description = TextAreaField("Description")

    submit = SubmitField("Add Income")
from wtforms import SelectField, DecimalField, IntegerField

class BudgetForm(FlaskForm):

    category = SelectField(
        "Category",
        choices=[
            ("Food","Food"),
            ("Travel","Travel"),
            ("Shopping","Shopping"),
            ("Medical","Medical"),
            ("Bills","Bills"),
            ("Education","Education"),
            ("Other","Other")
        ]
    )

    budget_amount = DecimalField(
        "Budget Amount",
        validators=[DataRequired()]
    )

    month = SelectField(
        "Month",
        choices=[
            ("January","January"),
            ("February","February"),
            ("March","March"),
            ("April","April"),
            ("May","May"),
            ("June","June"),
            ("July","July"),
            ("August","August"),
            ("September","September"),
            ("October","October"),
            ("November","November"),
            ("December","December")
        ]
    )

    year = IntegerField(
        "Year",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Budget")


from wtforms import SelectField

class InvestmentForm(FlaskForm):

    investment_type = SelectField(
        "Investment Type",
        choices=[
            ("Stocks", "Stocks"),
            ("Mutual Funds", "Mutual Funds"),
            ("Fixed Deposit", "Fixed Deposit"),
            ("Gold", "Gold"),
            ("Silver", "Silver"),
            ("Real Estate", "Real Estate"),
            ("Cryptocurrency", "Cryptocurrency"),
            ("PPF", "PPF"),
            ("EPF", "EPF"),
            ("NPS", "NPS"),
            ("Bonds", "Bonds"),
            ("Others", "Others")
        ]
    )

    investment_name = SelectField(
    "Investment Name",
    choices=[
        ("Reliance Industries", "Reliance Industries"),
        ("TCS", "TCS"),
        ("Infosys", "Infosys"),
        ("HDFC Bank", "HDFC Bank"),
        ("SBI Bluechip Fund", "SBI Bluechip Fund"),
        ("Axis Bluechip Fund", "Axis Bluechip Fund"),
        ("Gold ETF", "Gold ETF"),
        ("Bitcoin", "Bitcoin"),
        ("Ethereum", "Ethereum"),
        ("SBI Fixed Deposit", "SBI Fixed Deposit"),
        ("HDFC Fixed Deposit", "HDFC Fixed Deposit"),
        ("Public Provident Fund", "Public Provident Fund"),
        ("National Pension System", "National Pension System"),
        ("Others", "Others")
    ]
)
    amount = DecimalField("Investment Amount")
    current_value = DecimalField("Current Value")
    investment_date = DateField("Investment Date")
    submit = SubmitField("Save Investment")

class GoalForm(FlaskForm):

    goal_name = StringField(
        "Goal Name",
        validators=[DataRequired()]
    )

    target_amount = FloatField(
        "Target Amount",
        validators=[DataRequired()]
    )

    saved_amount = FloatField(
        "Saved Amount",
        validators=[DataRequired()]
    )

    target_date = DateField(
        "Target Date",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Goal")


