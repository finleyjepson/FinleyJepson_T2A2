from flask import Blueprint
import click
from flask.cli import with_appcontext
from .models import db, USER, Expense, Income
import os
import hashlib
import binascii
from datetime import date

cli_bp = Blueprint('db', __name__)

@click.command('init-db')
@with_appcontext
def init_db_command():
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

@click.command('reset-db')
@with_appcontext
def reset_db_command():
    db.drop_all()
    click.echo('Reset Database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    # Add a user
    salt = os.urandom(16)
    salt_hex = binascii.hexlify(salt).decode()

    passwords = ['Password0!', 'Password1!', 'Password2!']
    hashed_passwords = []
    salts = []

    for password in passwords:
        salt = os.urandom(16)
        salt_hex = binascii.hexlify(salt).decode()
        salts.append(salt_hex)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        hashed_password = binascii.hexlify(hashed_password).decode()
        hashed_passwords.append(hashed_password)

    user = [
        USER(
            username='admin', 
            password=hashed_passwords[0],
            salt=salts[0],
            is_admin=True
        ),
        USER(
            username='user1', 
            password=hashed_passwords[1],
            salt=salts[1],
            is_admin=False
        ),
        USER(
            username='user2', 
            password=hashed_passwords[2],
            salt=salts[2],
            is_admin=False
        )
    ]
    db.session.add_all(user)
    db.session.commit()

    # Add an expense
    expense = [
        # admin expenses
        Expense(userid=user[0].userid, amount=100, category='Groceries', date=date.now()),
        Expense(userid=user[0].userid, amount=50, category='Gas', date=date.now()),
        Expense(userid=user[0].userid, amount=200, category='Rent', date=date.now()),
        Expense(userid=user[0].userid, amount=100, category='Utilities', date=date.now()),
        Expense(userid=user[0].userid, amount=50, category='Entertainment', date=date.now()),
        # user1 expenses
        Expense(userid=user[1].userid, amount=120, category='Groceries', date=date.now()),
        Expense(userid=user[1].userid, amount=60, category='Gas', date=date.now()),
        Expense(userid=user[1].userid, amount=250, category='Rent', date=date.now()),
        Expense(userid=user[1].userid, amount=95, category='Utilities', date=date.now()),
        Expense(userid=user[1].userid, amount=40, category='Entertainment', date=date.now()),
        # user2 expenses
        Expense(userid=user[2].userid, amount=80, category='Groceries', date=date.now()),
        Expense(userid=user[2].userid, amount=40, category='Gas', date=date.now()),
        Expense(userid=user[2].userid, amount=150, category='Rent', date=date.now()),
        Expense(userid=user[2].userid, amount=75, category='Utilities', date=date.now()),
        Expense(userid=user[2].userid, amount=30, category='Entertainment', date=date.now())
    ]
    db.session.add_all(expense)
    db.session.commit()

    # Add an income
    income = [
        # admin income
        Income(userid=user[0].userid, amount=2000, source='Job', date=date.now()),
        Income(userid=user[0].userid, amount=100, source='Investments', date=date.now()),
        Income(userid=user[0].userid, amount=50, source='Other', date=date.now()),
        # user1 income
        Income(userid=user[1].userid, amount=1500, source='Job', date=date.now()),
        Income(userid=user[1].userid, amount=75, source='Investments', date=date.now()),
        Income(userid=user[1].userid, amount=30, source='Other', date=date.now()),
        # user2 income
        Income(userid=user[2].userid, amount=1000, source='Job', date=date.now()),
        Income(userid=user[2].userid, amount=50, source='Investments', date=date.now()),
        Income(userid=user[2].userid, amount=25, source='Other', date=date.now())
    ]
    db.session.add_all(income)
    db.session.commit()

    click.echo('Seeded the database.')

def init_app():
    cli_bp.cli.add_command(init_db_command)
    cli_bp.cli.add_command(seed_db_command)
    cli_bp.cli.add_command(reset_db_command)