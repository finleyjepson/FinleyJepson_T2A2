from flask import jsonify, session, Blueprint
from . import db
from flask import request
from .models import Income, Expense, Budget
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract

app = Blueprint('app', __name__)

@app.route('/expense', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def manage_expenses():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401
    match request.method:
        case 'POST':
            # Handle sending expenses
            amount = request.args.get('amount')
            category = request.args.get('category')
            new_expense = Expense(
                userid=session['userid'],
                amount=amount,
                category=category,
                date=datetime.now()
            )
            db.session.add(new_expense)
            db.session.commit()
            return jsonify({'message': 'Expense sent successfully'}), 200
        case 'DELETE':
            # Handle deleting expenses
            expense_id = request.args.get('expense_id')
            expense = Expense.query.filter_by(expenseid=expense_id, userid=session['userid']).first()
            if expense:
                db.session.delete(expense)
                db.session.commit()
                return jsonify({'message': 'Expense deleted successfully'}), 200
            else:
                return jsonify({'message': 'Expense not found'}), 404
        case 'PUT':
            # Handle editing expenses
            expense_id = request.args.get('expense_id')
            expense = Expense.query.filter_by(expenseid=expense_id, userid=session['userid']).first()
            if expense:
                expense_data = request.args
                expense.amount = expense_data.get('amount')
                expense.category = expense_data.get('category')
                db.session.commit()
                return jsonify({'message': 'Income updated successfully'}), 200
            else:
                return jsonify({'message': 'Income not found'}), 404
        case 'GET':
            # Handle getting expenses
            expenses = Expense.query.filter_by(userid=session['userid']).all()
            expense_list = []
            for expense in expenses:
                expense_data = {
                    'incomeid': expense.incomeid,
                    'amount': expense.amount,
                    'category': expense.category,
                    'date': expense.date
                }
                expense_list.append(expense_data)
            return jsonify(expense_list), 200
        case _:
            return jsonify({'message': 'Method not allowed'}), 405

@app.route('/income', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def manage_incomes():
    current_user = get_jwt_identity()
    match request.method:
        case 'POST':
            # Handle sending income
            amount = request.args.get('amount')
            source = request.args.get('source')
            new_income = Income(
                userid=current_user,
                amount=amount,
                source=source,
                date=datetime.now()
            )
            db.session.add(new_income)
            db.session.commit()
            return jsonify({'message': 'Income sent successfully'}), 200
        case 'DELETE':
            # Handle deleting income
            income_id = request.args.get('income_id')
            income = Income.query.filter_by(incomeid=income_id, userid=current_user).first()
            if income:
                db.session.delete(income)
                db.session.commit()
                return jsonify({'message': 'Income deleted successfully'}), 200
            else:
                return jsonify({'message': 'Income not found'}), 404
        case 'PUT':
            # Handle editing income
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
        case 'GET':
            # Handle getting income
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
        case _:
            return jsonify({'message': 'Method not allowed'}), 405

@app.route('/budget', methods=['POST'])
@jwt_required()
def create_budget():
    current_user = get_jwt_identity()
    current_year, current_month = datetime.now().year, datetime.now().month

    incomes = Income.query.filter(
        Income.userid == current_user, 
        extract('year', Income.date) == current_year, 
        extract('month', Income.date) == current_month
    ).all()
    total_income = 0
    for income in incomes:
        total_income += income.amount

    expenses = Expense.query.filter(
                    Expense.userid == current_user, 
                    extract('year', Expense.date) == current_year, 
                    extract('month', Expense.date) == current_month
                ).all()
    total_expense = 0
    for expense in expenses:
        total_expense += expense.amount

    total_budget = total_income - total_expense

    new_budget = Budget(userid=current_user, total_budget=total_budget, time_frame=str(current_year)+'-'+str(current_month))
    db.session.add(new_budget)
    db.session.commit()

    return jsonify(new_budget.to_dict()), 201

@app.route('/budget', methods=['GET'])
@jwt_required()
def get_budget():
    budget_id = request.args.get('id')
    budget = Budget.query.get(budget_id)
    return jsonify(budget), 200

@app.route('/budget/<int:id>', methods=['PUT'])
@jwt_required()
def update_budget(id):
    data = request.get_json()
    budget = Budget.query.get(id)
    budget.total_budget = data['total_budget']
    budget.time_frame = data['time_frame']
    db.session.commit()
    return jsonify(budget), 200

@app.route('/budget/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_budget(id):
    budget = Budget.query.get(id)
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'message': 'Budget deleted'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500