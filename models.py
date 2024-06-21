# backend/models.py

from db import db

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Numeric, nullable=False)
