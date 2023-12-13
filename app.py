from flask import jsonify, session, Blueprint
from . import db
from flask import request
from .models import Income, Expense, Budget
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint('app', __name__)

@app.route('/expense', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required
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
                category=category
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
@jwt_required
def manage_incomes():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401
    match request.method:
        case 'POST':
            # Handle sending income
            amount = request.args.get('amount')
            source = request.args.get('source')
            new_income = Income(
                userid=session['userid'],
                amount=amount,
                source=source
            )
            db.session.add(new_income)
            db.session.commit()
            return jsonify({'message': 'Income sent successfully'}), 200
        case 'DELETE':
            # Handle deleting income
            income_id = request.args.get('income_id')
            income = Income.query.filter_by(incomeid=income_id, userid=session['userid']).first()
            if income:
                db.session.delete(income)
                db.session.commit()
                return jsonify({'message': 'Income deleted successfully'}), 200
            else:
                return jsonify({'message': 'Income not found'}), 404
        case 'PUT':
            # Handle editing income
            income_id = request.args.get('income_id')
            income = Income.query.filter_by(incomeid=income_id, userid=session['userid']).first()
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
            incomes = Income.query.filter_by(userid=session['userid']).all()
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

@app.route('/budget', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required
def manage_budgets():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500