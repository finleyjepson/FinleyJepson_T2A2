from flask import jsonify, session, Blueprint
from . import db
from flask import request
from .models import Income, Expense, Budget
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract

app = Blueprint('app', __name__)


@app.route('/expense', methods=['POST'])
@jwt_required()
def create_expense():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    amount = request.args.get('amount')
    category = request.args.get('category')
    new_expense = Expense(
        userid=current_user,
        amount=amount,
        category=category
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense sent successfully'}), 200


@app.route('/expense', methods=['DELETE'])
@jwt_required()
def delete_expense():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    expense_id = request.args.get('expense_id')
    expense = Expense.query.filter_by(expenseid=expense_id, userid=current_user).first()
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    else:
        return jsonify({'message': 'Expense not found'}), 404


@app.route('/expense', methods=['PUT'])
@jwt_required()
def update_expense():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    expense_id = request.args.get('expense_id')
    expense = Expense.query.filter_by(expenseid=expense_id, userid=current_user).first()
    if expense:
        expense_data = request.args
        expense.amount = expense_data.get('amount')
        expense.category = expense_data.get('category')
        db.session.commit()
        return jsonify({'message': 'Expense updated successfully'}), 200
    else:
        return jsonify({'message': 'Expense not found'}), 404


@app.route('/expense', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    expense_id = request.args.get('expense_id')
    if expense_id:
        expenses = Expense.query.filter_by(userid=current_user, expenseid=expense_id).all()
    else:
        expenses = Expense.query.filter_by(userid=current_user).all()
    expense_list = []
    for expense in expenses:
        expense_data = {
            'expenseid': expense.expenseid,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date
        }
        expense_list.append(expense_data)
    return jsonify(expense_list), 200



@app.route('/income', methods=['POST'])
@jwt_required()
def create_income():
    current_user = get_jwt_identity()
    amount = request.args.get('amount')
    source = request.args.get('source')
    new_income = Income(
        userid=current_user,
        amount=amount,
        source=source
    )
    db.session.add(new_income)
    db.session.commit()
    return jsonify({'message': 'Income sent successfully'}), 200

@app.route('/income', methods=['GET'])
@jwt_required()
def get_incomes():
    current_user = get_jwt_identity()
    incomes = Income.query.filter_by(userid=current_user).all()
    income_list = []
    for income in incomes:
        income_data = {
            'incomeid': income.incomeid,
            'amount': income.amount,
            'source': income.source,
            'date': income.date
        }
        income_list.append(income_data)
    return jsonify(income_list), 200

@app.route('/income', methods=['PUT'])
@jwt_required()
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
        return jsonify({'message': 'Income not found'}), 404

@app.route('/income', methods=['DELETE'])
@jwt_required()
def delete_income():
    current_user = get_jwt_identity()
    income_id = request.args.get('income_id')
    income = Income.query.filter_by(incomeid=income_id, userid=current_user).first()
    if income:
        db.session.delete(income)
        db.session.commit()
        return jsonify({'message': 'Income deleted successfully'}), 200
    else:
        return jsonify({'message': 'Income not found'}), 404

@app.route('/budget', methods=['POST'])
@jwt_required()
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

    # Create a new budget entry in the database
    new_budget = Budget(userid=current_user, total_budget=total_budget, time_frame=str(current_year)+'-'+str(current_month))
    db.session.add(new_budget)
    db.session.commit()

    return jsonify(new_budget.to_dict()), 201

@app.route('/budget', methods=['GET'])
@jwt_required()
def get_budget():
    # Get the budgetid from the request arguments
    budget_id = request.args.get('budget_id')
    # Get the userid from the JWT token
    current_user = get_jwt_identity()

    if budget_id:
        # If budgetid is provided, filter budgets by userid and budgetid
        budgets = Budget.query.filter_by(userid=current_user, budgetid=budget_id).all()
    else:
        # If budgetid is not provided, filter budgets by userid only
        budgets = Budget.query.filter_by(userid=current_user).all()

    # Serialize the budgets into a JSON response
    return jsonify([budget.serialize() for budget in budgets]), 200

@app.route('/budget', methods=['PUT'])
@jwt_required()
def update_budget():
    current_user = get_jwt_identity()

    # Get the budget_id from the request arguments
    budget_id = request.args.get('budget_id')

    # Find the budget with the given budget_id and current_user
    budget = Budget.query.filter_by(budgetid=budget_id, userid=current_user).first()

    if budget:
        # Get the budget data from the request arguments
        budget_data = request.args

        # Update the budget amount and time frame
        budget.amount = budget_data.get('amount')
        budget.time_frame = budget_data.get('time_frame')
        budget.last_modified_date = date.now()
        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Budget updated successfully'}), 200
    else:
        # Return an error message if the budget is not found
        return jsonify({'message': 'Budget not found'}), 404

@app.route('/budget', methods=['DELETE'])
@jwt_required()
def delete_budget():
    current_user = get_jwt_identity()
    budget_id = request.args.get('budget_id')
    budget = Budget.query.filter_by(budgetid=budget_id, userid=current_user).first()
    if budget:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'}), 200
    else:
        return jsonify({'message': 'Budget not found'}), 404