from flask import Blueprint
import click
from flask.cli import with_appcontext
from .models import db, USER, Expense, Income, Budget
import os
import hashlib
import binascii
from datetime import datetime

cli_bp = Blueprint('db', __name__)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with some initial data."""

    
    # Add a user
    salt = os.urandom(16)
    salt_hex = binascii.hexlify(salt).decode()  # Convert salt to hexadecimal string

    passwords = ['password1', 'password2', 'password3']
    hashed_passwords = []
    salts = []

    for password in passwords:
        salt = os.urandom(16)
        salt_hex = binascii.hexlify(salt).decode()  # Convert salt to hexadecimal string
        salts.append(salt_hex)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        hashed_password = binascii.hexlify(hashed_password).decode()
        hashed_passwords.append(hashed_password)

    user = [
        USER(
            username='admin', 
            password=hashed_passwords[0], # hashed password with salt
            salt=salts[0], # salt used to hash the password
            is_admin=True
        ),
        USER(
            username='user1', 
            password=hashed_passwords[1], # hashed password with salt
            salt=salts[1], # salt used to hash the password
            is_admin=False
        ),
        USER(
            username='user2', 
            password=hashed_passwords[2], # hashed password with salt
            salt=salts[2], # salt used to hash the password
            is_admin=False
        )
    ]
    db.session.add_all(user)
    db.session.commit()

    # Add an expense
    expense = [
        # admin expenses
        Expense(userid=user[0].userid, amount=100, category='Groceries', date=datetime.now()),
        Expense(userid=user[0].userid, amount=50, category='Gas', date=datetime.now()),
        Expense(userid=user[0].userid, amount=200, category='Rent', date=datetime.now()),
        Expense(userid=user[0].userid, amount=100, category='Utilities', date=datetime.now()),
        Expense(userid=user[0].userid, amount=50, category='Entertainment', date=datetime.now()),
        # user1 expenses
        Expense(userid=user[1].userid, amount=120, category='Groceries', date=datetime.now()),
        Expense(userid=user[1].userid, amount=60, category='Gas', date=datetime.now()),
        Expense(userid=user[1].userid, amount=250, category='Rent', date=datetime.now()),
        Expense(userid=user[1].userid, amount=95, category='Utilities', date=datetime.now()),
        Expense(userid=user[1].userid, amount=40, category='Entertainment', date=datetime.now()),
        # user2 expenses
        Expense(userid=user[2].userid, amount=80, category='Groceries', date=datetime.now()),
        Expense(userid=user[2].userid, amount=40, category='Gas', date=datetime.now()),
        Expense(userid=user[2].userid, amount=150, category='Rent', date=datetime.now()),
        Expense(userid=user[2].userid, amount=75, category='Utilities', date=datetime.now()),
        Expense(userid=user[2].userid, amount=30, category='Entertainment', date=datetime.now())
    ]
    db.session.add_all(expense)
    db.session.commit()

    # Add an income
    income = [
        # admin income
        Income(userid=user[0].userid, amount=2000, source='Job', date=datetime.now()),
        Income(userid=user[0].userid, amount=100, source='Investments', date=datetime.now()),
        Income(userid=user[0].userid, amount=50, source='Other', date=datetime.now()),
        # user1 income
        Income(userid=user[1].userid, amount=1500, source='Job', date=datetime.now()),
        Income(userid=user[1].userid, amount=75, source='Investments', date=datetime.now()),
        Income(userid=user[1].userid, amount=30, source='Other', date=datetime.now()),
        # user2 income
        Income(userid=user[2].userid, amount=1000, source='Job', date=datetime.now()),
        Income(userid=user[2].userid, amount=50, source='Investments', date=datetime.now()),
        Income(userid=user[2].userid, amount=25, source='Other', date=datetime.now())
    ]
    db.session.add_all(income)
    db.session.commit()

    # Add a budget
    #budget = Budget(userid=user[0], total_budget=1500, time_frame='Monthly')
    #db.session.add(budget)

    click.echo('Seeded the database.')

def init_app():
    cli_bp.cli.add_command(init_db_command)
    cli_bp.cli.add_command(seed_db_command)