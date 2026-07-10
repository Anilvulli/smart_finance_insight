from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from app import app
from models import Expense, db, User,Income,Budget
from forms import ExpenseForm, ExpenseForm, RegisterForm, LoginForm, IncomeForm,BudgetForm
from sqlalchemy import func,desc,extract

@app.route("/")
def home():
    return redirect(url_for("login"))




@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256"
        )

        new_user = User(
            fullname=form.fullname.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            flash("Login Successful!", "success")

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid Email or Password", "danger")

    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():

    total_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id
    ).scalar() or 0

    total_expense = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0

    total_budget = db.session.query(func.sum(Budget.budget_amount)).filter(
        Budget.user_id == current_user.id
    ).scalar() or 0

    savings = total_income - total_expense

    recent_income = Income.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(Income.id)).limit(5).all()

    recent_expense = Expense.query.filter_by(
    user_id=current_user.id
    ).order_by(desc(Expense.expense_id)).limit(5).all()

    recent_budget = Budget.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(Budget.id)).limit(5).all()


    expense_data = db.session.query(
    Expense.category,
    func.sum(Expense.amount)
    ).filter(
    Expense.user_id == current_user.id
    ).group_by(Expense.category).all()

    labels = [row[0] for row in expense_data]
    values = [float(row[1]) for row in expense_data]
    # Monthly Income
    income_result = db.session.query(
        extract('month', Income.income_date),
        func.sum(Income.amount)
        ).filter(
            Income.user_id == current_user.id
            ).group_by(
                extract('month', Income.income_date)
                ).all()
    expense_result = db.session.query(
        extract('month', Expense.expense_date),
        func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id).group_by(
                extract('month', Expense.expense_date)
                ).all()
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    income_data = [0]*12
    expense_data = [0]*12
    for month, amount in income_result:
        income_data[int(month)-1] = float(amount)
        for month, amount in expense_result:
            expense_data[int(month)-1] = float(amount)
    

    return render_template(
    "dashboard.html",
    total_income=total_income,
    total_expense=total_expense,
    total_budget=total_budget,
    savings=savings,
    recent_income=recent_income,
    recent_expense=recent_expense,
    recent_budget=recent_budget,
    labels=labels,
    values=values,
    months=months,
    income_data=income_data,
    expense_data=expense_data
)
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully", "info")

    return redirect(url_for("login"))

@app.route("/expense", methods=["GET","POST"])
@login_required
def expense():

    form = ExpenseForm()

    if form.validate_on_submit():

        expense = Expense(

            user_id=current_user.id,

            category=form.category.data,

            amount=form.amount.data,

            payment_method=form.payment_method.data,

            expense_date=form.expense_date.data,

            description=form.description.data

        )

        db.session.add(expense)

        db.session.commit()

        flash("Expense Added Successfully")

        return redirect(url_for("expense"))

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "expense.html",
        form=form,
        expenses=expenses
    )


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():

    form = IncomeForm()

    if form.validate_on_submit():

        data = Income(
            user_id=current_user.id,
            source=form.source.data,
            amount=form.amount.data,
            income_date=form.income_date.data,
            description=form.description.data
        )

        db.session.add(data)
        db.session.commit()

        flash("Income Added Successfully", "success")

        return redirect(url_for("income"))

    incomes = Income.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "income.html",
        form=form,
        incomes=incomes
    )



@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():

    form = BudgetForm()

    if form.validate_on_submit():

        budget = Budget(
            user_id=current_user.id,
            category=form.category.data,
            budget_amount=form.budget_amount.data,
            month=form.month.data,
            year=form.year.data
        )

        db.session.add(budget)
        db.session.commit()

        flash("Budget Saved Successfully!", "success")

        return redirect(url_for("budget"))

    budgets = Budget.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "budget.html",
        form=form,
        budgets=budgets
    )

# from sqlalchemy import func
# from flask_login import login_required, current_user
# from models import Income, Expense, Budget

@app.route("/reports")
@login_required
def reports():

    total_income = db.session.query(
        func.sum(Income.amount)
    ).filter(
        Income.user_id == current_user.id
    ).scalar() or 0

    total_expense = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0

    total_budget = db.session.query(
        func.sum(Budget.budget_amount)
    ).filter(
        Budget.user_id == current_user.id
    ).scalar() or 0

    savings = total_income - total_expense

    income_list = Income.query.filter_by(
        user_id=current_user.id
    ).all()

    expense_list = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    budget_list = Budget.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "reports.html",
        total_income=total_income,
        total_expense=total_expense,
        total_budget=total_budget,
        savings=savings,
        income_list=income_list,
        expense_list=expense_list,
        budget_list=budget_list
    )