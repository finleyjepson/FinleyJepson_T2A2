from flask import jsonify, session, Blueprint
from . import db

app = Blueprint('app', __name__)

@app.route('/expenses', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_expenses():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/incomes', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_incomes():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/budgets', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_budgets():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500