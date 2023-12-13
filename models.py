from . import db

class USER(db.Model):
    __tablename__ = 'USER'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)

class Session(db.Model):
    __tablename__ = 'session'
    sessionid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    token = db.Column(db.String(255))
    startTime = db.Column(db.TIMESTAMP)
    endTime = db.Column(db.TIMESTAMP)

class Expense(db.Model):
    __tablename__ = 'expense'
    expenseid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    category = db.Column(db.String(255))
    date = db.Column(db.DATE)
    notes = db.Column(db.TEXT)

class Income(db.Model):
    __tablename__ = 'income'
    incomeid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    amount = db.Column(db.Integer)
    source = db.Column(db.String(255))
    date = db.Column(db.DATE)

class Budget(db.Model):
    __tablename__ = 'budget'
    budgetid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2))
    category = db.Column(db.String(255))
    timeframe = db.Column(db.String(255))