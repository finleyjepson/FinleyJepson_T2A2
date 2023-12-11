from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

class USER(db.Model):
    __tablename__ = 'USER'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(45), nullable=False)

class Session(db.Model):
    __tablename__ = 'session'
    sessionID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    token = db.Column(db.String(255))
    startTime = db.Column(db.TIMESTAMP)
    endTime = db.Column(db.TIMESTAMP)

class Expense(db.Model):
    __tablename__ = 'expense'
    expenseID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    category = db.Column(db.String(255))
    date = db.Column(db.DATE)
    notes = db.Column(db.TEXT)

class Income(db.Model):
    __tablename__ = 'income'
    incomeID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    source = db.Column(db.String(255))
    date = db.Column(db.DATE)

class Budget(db.Model):
    __tablename__ = 'budget'
    budgetID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    category = db.Column(db.String(255))
    timeFrame = db.Column(db.String(255))

@app.route('/register', methods=['POST'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if the username already exists in the database
    existing_user = USER.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user
    new_user = USER(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    pass

@app.route('/expenses', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_expenses():
    pass

@app.route('/incomes', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_incomes():
    pass

@app.route('/budgets', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_budgets():
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)