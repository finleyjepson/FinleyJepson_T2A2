from functools import wraps 
from flask import jsonify, session, Blueprint 
from . import db 
from flask import request 
from .models import Income, Expense, Budget 
from datetime import date 
from flask_jwt_extended import jwt_required, get_jwt_identity 
from sqlalchemy import extract

app = Blueprint('app', __name__)

# Decorator to require JWT authentication and user identity
def jwt_required_and_user(f): 
    @wraps(f) 
    @jwt_required()
    def decorated(*args, **kwargs): 
        current_user = get_jwt_identity() 
        if not current_user: 
            return jsonify({'message': 'Unauthorized'}), 401 
        return f(*args, **kwargs) 
    return decorated

# Helper function to handle not found entities
def handle_not_found(entity): 
    return jsonify({'message': f'{entity} not found'}), 404

# Helper function to create a new entity
def create_entity(entity_class, **kwargs): 
    new_entity = entity_class(**kwargs) 
    db.session.add(new_entity) 
    db.session.commit()
    return new_entity

# Route to create an expense
@app.route('/expense', methods=['POST']) 
@jwt_required_and_user 
def create_expense(): 
    current_user = get_jwt_identity() 
    amount = request.args.get('amount') 
    category = request.args.get('category') 
    create_entity(Expense, userid=current_user, amount=amount, category=category) 
    return jsonify({'message': 'Expense sent successfully'}), 200

# Route to delete an expense
@app.route('/expense', methods=['DELETE']) 
@jwt_required_and_user 
def delete_expense(): 
    current_user = get_jwt_identity() 
    expense_id = request.args.get('expense_id') 
    expense = Expense.query.filter_by(expenseid=expense_id, userid=current_user).first() 
    if expense: 
        db.session.delete(expense)
        db.session.commit() 
        return jsonify({'message': 'Expense deleted successfully'}), 200 
    else: 
        return handle_not_found('Expense')

# Route to update an expense
@app.route('/expense', methods=['PUT']) 
@jwt_required_and_user 
def update_expense(): 
    current_user = get_jwt_identity() 
    expense_id = request.args.get('expense_id') 
    expense = Expense.query.filter_by(expenseid=expense_id, userid=current_user).first() 
    if expense: 
        expense_data = request.args 
        expense.amount = expense_data.get('amount') 
        expense.category = expense_data.get('category') 
        db.session.commit() 
        return jsonify({'message': 'Expense updated successfully'}), 200 
    else: 
        return handle_not_found('Expense')

# Route to get expenses
@app.route('/expense', methods=['GET']) 
@jwt_required_and_user 
def get_expenses(): 
    # Get the current user's identity from the JWT token
    current_user = get_jwt_identity() 
    # Get the expense ID from the request parameters
    expense_id = request.args.get('expense_id') 
    # Check if an expense ID is provided
    if expense_id: 
        expenses = Expense.query.filter_by(userid=current_user, expenseid=expense_id).all() 
    else: 
        expenses = Expense.query.filter_by(userid=current_user).all() 
    expense_list = [] 
    # Convert the expenses to a list of dictionaries
    for expense in expenses: 
        expense_data = { 'expenseid': expense.expenseid, 'amount': expense.amount, 'category': expense.category, 'date': expense.date } 
        expense_list.append(expense_data) 
    return jsonify(expense_list), 200

# Route to create an income
@app.route('/income', methods=['POST']) 
@jwt_required_and_user 
def create_income(): 
    current_user = get_jwt_identity() 
    amount = request.args.get('amount') 
    source = request.args.get('source') 
    create_entity(Income, userid=current_user, amount=amount, source=source) 
    return jsonify({'message': 'Income sent successfully'}), 200

# Route to get incomes
@app.route('/income', methods=['GET']) 
@jwt_required_and_user 
def get_incomes(): 
    current_user = get_jwt_identity() 
    incomes = Income.query.filter_by(userid=current_user).all() 
    income_list = [] 
    for income in incomes: 
        income_data = { 'incomeid': income.incomeid, 'amount': income.amount, 'source': income.source, 'date': income.date } 
        income_list.append(income_data) 
    return jsonify(income_list), 200

# Route to update an income
@app.route('/income', methods=['PUT']) 
@jwt_required_and_user 
def update_income(): 
    current_user = get_jwt_identity() 
    income_id = request.args.get('income_id') 
    income = Income.query.filter_by(incomeid=income_id, userid=current_user).first() 
    if income: 
        income_data = request.args 
        income.amount = income_data.get('amount') 
        income.source = income_data.get('source') 
        db.session.commit() 
        return jsonify({'message': 'Income updated successfully'}), 200 
    else: 
        return handle_not_found('Income')

# Route to delete an income
@app.route('/income', methods=['DELETE']) 
@jwt_required_and_user 
def delete_income(): 
    current_user = get_jwt_identity() 
    income_id = request.args.get('income_id') 
    income = Income.query.filter_by(incomeid=income_id, userid=current_user).first() 
    if income:
        db.session.delete(income) 
        db.session.commit() 
        return jsonify({'message': 'Income deleted successfully'}), 200 
    else:
        return handle_not_found('Income')

# Route to create a budget
@app.route('/budget', methods=['POST']) 
@jwt_required_and_user 
def create_budget(): 
    current_user = get_jwt_identity() 
    current_year, current_month = date.now().year, date.now().month
    
    # Calculate total income for the current month
    incomes = Income.query.filter(
        Income.userid == current_user, 
        extract('year', Income.date) == current_year, 
        extract('month', Income.date) == current_month
    ).all()
    total_income = 0
    for income in incomes:
        total_income += income.amount
    
    # Calculate total expense for the current month
    expenses = Expense.query.filter(
        Expense.userid == current_user, 
        extract('year', Expense.date) == current_year, 
        extract('month', Expense.date) == current_month
    ).all()
    total_expense = 0
    for expense in expenses:
        total_expense += expense.amount
    
    # Calculate total budget for the current month
    total_budget = total_income - total_expense
    
    # Create a new budget entity
    create_entity(Budget, userid=current_user, total_budget=total_budget, time_frame=str(current_year)+'-'+str(current_month))
    
    return jsonify({'message': 'Budget created successfully'}), 201

# Route to get budgets
@app.route('/budget', methods=['GET']) 
@jwt_required_and_user 
def get_budget():
    budget_id = request.args.get('budget_id')
    current_user = get_jwt_identity()
    if budget_id:
        budgets = Budget.query.filter_by(userid=current_user, budgetid=budget_id).all()
    else:
        budgets = Budget.query.filter_by(userid=current_user).all()
    return jsonify([budget.serialize() for budget in budgets]), 200

# Route to update a budget
@app.route('/budget', methods=['PUT'])
@jwt_required_and_user
def update_budget():
    current_user = get_jwt_identity()
    budget_id = request.args.get('budget_id')
    budget = Budget.query.filter_by(budgetid=budget_id, userid=current_user).first()
    if budget:
        budget_data = request.args
        budget.amount = budget_data.get('amount')
        budget.time_frame = budget_data.get('time_frame')
        budget.last_modified_date = date.now()
        db.session.commit()
        return jsonify({'message': 'Budget updated successfully'}), 200
    else:
        return handle_not_found('Budget')

# Route to delete a budget
@app.route('/budget', methods=['DELETE'])
@jwt_required_and_user
def delete_budget():
    current_user = get_jwt_identity()
    budget_id = request.args.get('budget_id')
    budget = Budget.query.filter_by(budgetid=budget_id, userid=current_user).first()
    if budget:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'}), 200
    else:
        return handle_not_found('Budget')