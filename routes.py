from flask import render_template, redirect, url_for, flash,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from app import app
from models import Expense, db, User,Income,Budget,Investment, Goal
from forms import ExpenseForm, ExpenseForm, RegisterForm, LoginForm, IncomeForm,BudgetForm,InvestmentForm,GoalForm
from sqlalchemy import func,desc,extract
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from io import BytesIO


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

    recent_income = Income.query.filter_by(
        user_id=current_user.id
    ).order_by(
        desc(Income.id)
    ).limit(5).all()

    recent_expense = Expense.query.filter_by(
        user_id=current_user.id
    ).order_by(
        desc(Expense.expense_id)
    ).limit(5).all()

    recent_budget = Budget.query.filter_by(
        user_id=current_user.id
    ).order_by(
        desc(Budget.id)
    ).limit(5).all()

   
    expense_chart = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id
    ).group_by(
        Expense.category
    ).all()

    labels = []
    values = []

    for row in expense_chart:
        labels.append(row[0])
        values.append(float(row[1]))

  
    months = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    income_data = [0]*12
    expense_data = [0]*12

    income_result = db.session.query(
        extract('month', Income.income_date),
        func.sum(Income.amount)
    ).filter(
        Income.user_id==current_user.id
    ).group_by(
        extract('month', Income.income_date)
    ).all()

    for month, amount in income_result:
        income_data[int(month)-1]=float(amount)

    expense_result = db.session.query(
        extract('month', Expense.expense_date),
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id==current_user.id
    ).group_by(
        extract('month', Expense.expense_date)
    ).all()

    for month, amount in expense_result:
        expense_data[int(month)-1]=float(amount)

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
        expense_data=expense_data,

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


@app.route("/investment", methods=["GET", "POST"])
@login_required
def investment():

    form = InvestmentForm()

    if form.validate_on_submit():

        investment = Investment(
            user_id=current_user.id,
            investment_type=form.investment_type.data,
            investment_name=form.investment_name.data,
            amount=form.amount.data,
            current_value=form.current_value.data,
            investment_date=form.investment_date.data
        )

        db.session.add(investment)
        db.session.commit()

        flash("Investment Added Successfully!", "success")
        return redirect(url_for("investment"))

    investments = Investment.query.filter_by(
        user_id=current_user.id
    ).all()

    total_investment = sum(float(i.amount or 0) for i in investments)

    total_current = sum(float(i.current_value or 0) for i in investments)

    total_profit = total_current - total_investment

    roi = round(
        (total_profit / total_investment) * 100, 2
    ) if total_investment > 0 else 0

    chart_data = db.session.query(
        Investment.investment_type,
        func.sum(Investment.current_value)
    ).filter(
        Investment.user_id == current_user.id
    ).group_by(
        Investment.investment_type
    ).all()

    labels = []
    values = []
    percentages = []

    for asset_type, amount in chart_data:

        labels.append(asset_type)

        amount = float(amount)

        values.append(amount)

        percentages.append(
            round((amount / total_current) * 100, 2)
            if total_current > 0 else 0
        )

    investment_names = [
        inv.investment_name for inv in investments
    ]

    invested_amounts = [
        float(inv.amount) for inv in investments
    ]

    current_values = [
        float(inv.current_value) for inv in investments
    ]

    profits = [
        float(inv.current_value - inv.amount)
        for inv in investments
    ]

    top_asset = None

    if investments:
        top_asset = max(
            investments,
            key=lambda x: x.current_value - x.amount
        )

    
    diversification = []

    for inv in investments:

        profit = float(inv.current_value - inv.amount)

        investment_roi = (
            round((profit / inv.amount) * 100, 2)
            if inv.amount > 0 else 0
        )

        allocation = (
            round((inv.current_value / total_current) * 100, 2)
            if total_current > 0 else 0
        )

        diversification.append({
            "name": inv.investment_name,
            "type": inv.investment_type,
            "invested": float(inv.amount),
            "current": float(inv.current_value),
            "profit": profit,
            "roi": investment_roi,
            "allocation": allocation
        })

    return render_template(
        "investment.html",
        form=form,
        investments=investments,
        total_investment=total_investment,
        total_current=total_current,
        total_profit=total_profit,
        roi=roi,
        labels=labels,
        values=values,
        percentages=percentages,
        investment_names=investment_names,
        invested_amounts=invested_amounts,
        current_values=current_values,
        profits=profits,
        diversification=diversification,
        top_asset=top_asset
    )

    


@app.route("/goal", methods=["GET", "POST"])
@login_required
def goal():

    form = GoalForm()
    if form.validate_on_submit():

        new_goal = Goal(

            user_id=current_user.id,
            goal_name=form.goal_name.data,
            target_amount=form.target_amount.data,
            saved_amount=form.saved_amount.data,
            target_date=form.target_date.data

        )

        db.session.add(new_goal)
        db.session.commit()

        flash("Financial Goal Added Successfully!", "success")

        return redirect(url_for("goal"))
    goals = Goal.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Goal.target_date.asc()
    ).all()

    total_target = sum(float(g.target_amount or 0) for g in goals)

    total_saved = sum(float(g.saved_amount or 0) for g in goals)

    remaining_amount = total_target - total_saved

    if total_target > 0:
        overall_progress = round(
            (total_saved / total_target) * 100,
            2
        )
    else:
        overall_progress = 0


    goal_labels = []
    goal_progress = []

    for g in goals:

        goal_labels.append(g.goal_name)

        if g.target_amount > 0:

            progress = round(
                (g.saved_amount / g.target_amount) * 100,
                2
            )

        else:

            progress = 0

        goal_progress.append(progress)

    top_goal = None

    if goals:

        top_goal = min(
            goals,
            key=lambda x: x.target_date
        )

    analytics = []

    for g in goals:

        saved = float(g.saved_amount or 0)

        target = float(g.target_amount or 0)

        remaining = target - saved

        if target > 0:
            progress = round(
                (saved / target) * 100,
                2
            )
        else:
            progress = 0

        if progress >= 100:
            status = "Completed"

        elif progress >= 75:
            status = "Almost There"

        elif progress >= 40:
            status = "In Progress"

        else:
            status = "Started"

        analytics.append({

            "goal_name": g.goal_name,

            "target": target,

            "saved": saved,

            "remaining": remaining,

            "progress": progress,

            "status": status,

            "target_date": g.target_date

        })


    return render_template(

        "goal.html",

        form=form,

        goals=goals,

        goal_labels=goal_labels,

        goal_progress=goal_progress,

        total_target=total_target,

        total_saved=total_saved,

        remaining_amount=remaining_amount,

        overall_progress=overall_progress,

        top_goal=top_goal,

        analytics=analytics

    )



@app.route("/portfolio")
@login_required
def portfolio():

    investments = Investment.query.filter_by(
        user_id=current_user.id
    ).all()

    goals = Goal.query.filter_by(
        user_id=current_user.id
    ).all()

    total_goals = len(goals)

    completed = len([
        g for g in goals
        if g.saved_amount >= g.target_amount
    ])

    goal_percentage = round(
        (completed / total_goals) * 100,
        2
    ) if total_goals else 0

   
    total_investment = sum(float(i.amount) for i in investments)

    total_current = sum(float(i.current_value) for i in investments)

    total_profit = total_current - total_investment

    roi = round(
        (total_profit / total_investment) * 100,
        2
    ) if total_investment else 0
    asset_data = db.session.query(

        Investment.investment_type,

        func.sum(Investment.current_value)

    ).filter(

        Investment.user_id == current_user.id

    ).group_by(

        Investment.investment_type

    ).all()

    asset_labels = []

    asset_values = []

    for name, value in asset_data:

        asset_labels.append(name)

        asset_values.append(float(value))
        monthly = db.session.query(
        func.date_format(
            Investment.investment_date,
            "%Y-%m"
            ),
        func.sum(Investment.current_value)
        ).filter(
        Investment.user_id == current_user.id
        ).group_by(
        func.date_format(
            Investment.investment_date,
            "%Y-%m"
        )
        ).all()
    months = []
    growth = []

    for month, value in monthly:
        months.append(month)
        growth.append(float(value))
    
        top_asset = None
        worst_asset = None

    if investments:

        top_asset = max(
            investments,
            key=lambda x: x.current_value - x.amount
        )

        worst_asset = min(
            investments,
            key=lambda x: x.current_value - x.amount
        )
        total_goals = len(goals)

    completed = len([
        g for g in goals
        if g.saved_amount >= g.target_amount
    ])

    goal_percentage = round(

        (completed / total_goals) * 100,

        2

    ) if total_goals else 0
    
    risk = "Low"
    crypto = 0
    stocks = 0

    for i in investments:

        if i.investment_type == "Cryptocurrency":
            crypto += 1

        if i.investment_type == "Stocks":
            stocks += 1

    if crypto >= 2:
        risk = "High"

    elif stocks >= 2:
        risk = "Medium"

    diversification = []

    for inv in investments:

        allocation = round(

            (float(inv.current_value) / total_current) * 100,

            2

        ) if total_current else 0

        diversification.append({

            "name": inv.investment_name,

            "type": inv.investment_type,

            "allocation": allocation

        })
        return render_template(

        "portfolio.html",

        total_investment=total_investment,

        total_current=total_current,

        total_profit=total_profit,

        roi=roi,

        asset_labels=asset_labels,

        asset_values=asset_values,

        months=months,

        growth=growth,

        diversification=diversification,

        top_asset=top_asset,

        worst_asset=worst_asset,

        total_goals=total_goals,

        completed=completed,

        goal_percentage=goal_percentage,

        risk=risk

    )



@app.route("/download_pdf")
@login_required
def download_pdf():

    investments = Investment.query.filter_by(
        user_id=current_user.id
    ).all()

    total_investment = sum(float(i.amount) for i in investments)
    total_current = sum(float(i.current_value) for i in investments)
    total_profit = total_current - total_investment

    roi = round(
        (total_profit / total_investment) * 100,
        2
    ) if total_investment else 0

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Smart Finance Insights</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Portfolio Analytics Report",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["BodyText"])
    )

    summary = [

        ["Total Investment", f"₹ {total_investment:,.2f}"],

        ["Current Value", f"₹ {total_current:,.2f}"],

        ["Profit / Loss", f"₹ {total_profit:,.2f}"],

        ["Overall ROI", f"{roi}%"]

    ]

    table = Table(summary, colWidths=[3*inch,2.5*inch])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.grey),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

        ("TEXTCOLOR",(0,0),(-1,-1),colors.black),

        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    elements.append(table)

    elements.append(
        Paragraph("<br/><b>Investment Details</b>", styles["Heading2"])
    )

    data = [[
        "Type",
        "Name",
        "Investment",
        "Current",
        "Profit"
    ]]

    for inv in investments:

        data.append([

            inv.investment_type,

            inv.investment_name,

            f"₹ {inv.amount}",

            f"₹ {inv.current_value}",

            f"₹ {inv.current_value-inv.amount}"

        ])

    investment_table = Table(data)

    investment_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    elements.append(investment_table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=Portfolio_Report.pdf"

    return response




@app.route("/download_excel")
@login_required
def download_excel():

    investments = Investment.query.filter_by(
        user_id=current_user.id
    ).all()

    total_investment = sum(float(i.amount) for i in investments)
    total_current = sum(float(i.current_value) for i in investments)
    total_profit = total_current - total_investment

    roi = round(
        (total_profit / total_investment) * 100,
        2
    ) if total_investment > 0 else 0

    wb = Workbook()

    ws = wb.active

    ws.title = "Portfolio Report"

    # Title
    ws["A1"] = "Smart Finance Insights"
    ws["A1"].font = Font(size=18, bold=True)

    ws["A2"] = "Portfolio Analytics Report"
    ws["A2"].font = Font(size=14, bold=True)

  
    ws["A4"] = "Total Investment"
    ws["B4"] = total_investment

    ws["A5"] = "Current Value"
    ws["B5"] = total_current

    ws["A6"] = "Profit / Loss"
    ws["B6"] = total_profit

    ws["A7"] = "Overall ROI (%)"
    ws["B7"] = roi

    row = 10

    headings = [
        "Investment Type",
        "Investment Name",
        "Investment Amount",
        "Current Value",
        "Profit / Loss",
        "ROI (%)"
    ]

    fill = PatternFill(
        start_color="1F4E78",
        end_color="1F4E78",
        fill_type="solid"
    )

    for col, heading in enumerate(headings, start=1):

        cell = ws.cell(row=row, column=col)

        cell.value = heading

        cell.font = Font(bold=True, color="FFFFFF")

        cell.fill = fill

    row += 1

    for inv in investments:

        profit = float(inv.current_value - inv.amount)

        investment_roi = round(
            (profit / inv.amount) * 100,
            2
        ) if inv.amount > 0 else 0

        ws.cell(row=row, column=1).value = inv.investment_type
        ws.cell(row=row, column=2).value = inv.investment_name
        ws.cell(row=row, column=3).value = float(inv.amount)
        ws.cell(row=row, column=4).value = float(inv.current_value)
        ws.cell(row=row, column=5).value = profit
        ws.cell(row=row, column=6).value = investment_roi

        row += 1

    
    for column_cells in ws.columns:

        length = max(len(str(cell.value or "")) for cell in column_cells)

        ws.column_dimensions[column_cells[0].column_letter].width = length + 5

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    response = make_response(output.getvalue())

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=Portfolio_Report.xlsx"

    response.headers[
        "Content-Type"
    ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response