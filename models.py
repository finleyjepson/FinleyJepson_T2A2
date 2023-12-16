from . import db

class USER(db.Model):
    __tablename__ = 'USER'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class Expense(db.Model):
    __tablename__ = 'expense'
    expenseid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    amount = db.Column(db.Integer)
    category = db.Column(db.String(255))
    date = db.Column(db.DATE, nullable=False, default=db.func.current_date())

    def to_dict(self):
        return {
            'expenseid': self.expenseid,
            'userid': self.userid,
            'amount': self.amount,
            'category': self.category,
            'date': self.date
        }

class Income(db.Model):
    __tablename__ = 'income'
    incomeid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    amount = db.Column(db.Integer)
    source = db.Column(db.String(255))
    date = db.Column(db.DATE, nullable=False, default=db.func.current_date())

    def to_dict(self):
        return {
            'incomeid': self.incomeid,
            'userid': self.userid,
            'amount': self.amount,
            'source': self.source,
            'date': self.date
        }
    

class Budget(db.Model):
    __tablename__ = 'budgets'
    budgetid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('USER.userid'), nullable=False)
    total_budget = db.Column(db.Integer, nullable=False)
    time_frame = db.Column(db.String(50))
    creation_date = db.Column(db.DATE, nullable=False, default=db.func.current_date())
    last_modified_date = db.Column(db.DATE, nullable=False, default=db.func.current_date())

    def to_dict(self):
        return {
            'budgetid': self.budgetid,
            'userid': self.userid,
            'total_budget': self.total_budget,
            'time_frame': self.time_frame,
            'creation_date': self.creation_date,
            'last_modified_date': self.last_modified_date
        }