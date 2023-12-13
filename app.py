from flask import jsonify, session, Blueprint
from . import db
from flask import request
from .models import Income, Expense, Budget, USER
from datetime import datetime
from datetime import datetime

app = Blueprint('app', __name__)

@app.route('/expense', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_expenses():
    if 'userid' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/income', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_incomes():
    if 'userid' not in session:
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
def manage_budgets():
    if 'userid' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500