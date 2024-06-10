from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint('routes', __name__)

@bp.route('/api/query', methods=['POST'])
def query():
    question = request.json['question'].lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    chart_data = {'labels': [], 'data': []}
    answer = ""

    if "average salary by department" in question:
        cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
        data = cursor.fetchall()
        for row in data:
            chart_data['labels'].append(row[0])
            chart_data['data'].append(row[1])
        answer = "Average salary by department"
    elif "total salary expenditure by department" in question:
        cursor.execute("SELECT department, SUM(salary) FROM employees GROUP BY department")
        data = cursor.fetchall()
        for row in data:
            chart_data['labels'].append(row[0])
            chart_data['data'].append(row[1])
        answer = "Total salary expenditure by department"
    elif "number of employees by department" in question:
        cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
        data = cursor.fetchall()
        for row in data:
            chart_data['labels'].append(row[0])
            chart_data['data'].append(row[1])
        answer = "Number of employees by department"
    else:
        answer = "Sorry, I didn't understand the question."

    conn.close()
    return jsonify({'answer': answer, 'chart_data': chart_data})

@bp.route('/api/stats', methods=['GET'])
def stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
    data = cursor.fetchall()
    conn.close()

    result = {'labels': [], 'data': []}
    for row in data:
        result['labels'].append(row[0])
        result['data'].append(row[1])
    
    return jsonify(result)
