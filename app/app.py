from flask import Flask
import settings
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'))
db = SQLAlchemy(app)
