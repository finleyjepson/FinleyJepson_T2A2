from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

