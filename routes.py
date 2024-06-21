from flask import Blueprint, request, jsonify
from models import db, Employee
from sqlalchemy.sql import func, case
import re

bp = Blueprint('routes', __name__)

@bp.route('/api/query', methods=['POST'])
def query():
    question = request.json.get('question', '').lower()
    
    # Define keyword mappings to SQLAlchemy functions and model fields
    keyword_map = {
        'average': func.avg,
        'total': func.sum,
        'number': func.count,
        'many': func.count,  # 'many' is treated as synonymous with 'number'
        'salary': Employee.salary,
        'age': Employee.age,
        'department': Employee.department,
        'position': Employee.position,
        'employees': func.count
    }
    
    # Define keyword combinations and their corresponding SQL queries
    keyword_combinations = {
        ('average', 'salary', 'department'): {
            'query': db.session.query(Employee.department, func.avg(Employee.salary)).group_by(Employee.department).all(),
            'label': 'Average salary by department'
        },
        ('total', 'salary', 'department'): {
            'query': db.session.query(Employee.department, func.sum(Employee.salary)).group_by(Employee.department).all(),
            'label': 'Total salary expenditure by department'
        },
        ('number', 'employees', 'department'): {
            'query': db.session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all(),
            'label': 'Number of employees by department'
        },
        ('average', 'age', 'department'): {
            'query': db.session.query(Employee.department, func.avg(Employee.age)).group_by(Employee.department).all(),
            'label': 'Average age by department'
        },
        ('average', 'salary', 'position'): {
            'query': db.session.query(Employee.position, func.avg(Employee.salary)).group_by(Employee.position).all(),
            'label': 'Average salary by position'
        },
        ('total', 'salary', 'position'): {
            'query': db.session.query(Employee.position, func.sum(Employee.salary)).group_by(Employee.position).all(),
            'label': 'Total salary expenditure by position'
        },
        ('number', 'employees', 'position'): {
            'query': db.session.query(Employee.position, func.count(Employee.id)).group_by(Employee.position).all(),
            'label': 'Number of employees by position'
        },
        ('average', 'age', 'position'): {
            'query': db.session.query(Employee.position, func.avg(Employee.age)).group_by(Employee.position).all(),
            'label': 'Average age by position'
        },
        ('salary', 'distribution', 'age'): {
            'query': db.session.query(Employee.age, func.avg(Employee.salary)).group_by(Employee.age).all(),
            'label': 'Salary distribution by age'
        },
        ('employee', 'count', 'age', 'range'): {
            'query': {
                '20-29': db.session.query(func.count(Employee.id)).filter(Employee.age.between(20, 29)).scalar(),
                '30-39': db.session.query(func.count(Employee.id)).filter(Employee.age.between(30, 39)).scalar(),
                '40-49': db.session.query(func.count(Employee.id)).filter(Employee.age.between(40, 49)).scalar(),
                '50-59': db.session.query(func.count(Employee.id)).filter(Employee.age.between(50, 59)).scalar(),
                '60+': db.session.query(func.count(Employee.id)).filter(Employee.age >= 60).scalar()
            },
            'label': 'Employee count by age range'
        },
        ('total', 'salary', 'age', 'range'): {
            'query': {
                '20-29': db.session.query(func.sum(Employee.salary)).filter(Employee.age.between(20, 29)).scalar(),
                '30-39': db.session.query(func.sum(Employee.salary)).filter(Employee.age.between(30, 39)).scalar(),
                '40-49': db.session.query(func.sum(Employee.salary)).filter(Employee.age.between(40, 49)).scalar(),
                '50-59': db.session.query(func.sum(Employee.salary)).filter(Employee.age.between(50, 59)).scalar(),
                '60+': db.session.query(func.sum(Employee.salary)).filter(Employee.age >= 60).scalar()
            },
            'label': 'Total salary expenditure by age range'
        }
        # Add more combinations as needed
    }
    
    # Extract keywords from the question
    extracted_keywords = [kw for kw in keyword_map.keys() if re.search(kw, question)]
    
    # Identify matching keyword combination
    matched_combination = None
    for keywords, data in keyword_combinations.items():
        if all(kw in extracted_keywords for kw in keywords):
            matched_combination = keywords
            break
    
    # If no combination matched, return an error response
    if not matched_combination:
        return jsonify({'answer': "Sorry, I didn't understand the question.", 'chart_data': {}})
    
    # Execute SQL query based on matched combination
    chart_data = {'labels': [], 'data': []}
    answer = keyword_combinations[matched_combination]['label']
    query_data = keyword_combinations[matched_combination]['query']
    
    if isinstance(query_data, list):
        chart_data['labels'], chart_data['data'] = zip(*query_data)
    elif isinstance(query_data, dict):
        chart_data['labels'], chart_data['data'] = zip(*query_data.items())
    
    return jsonify({'answer': answer, 'chart_data': chart_data})
