from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Store collections in memory (for simplicity)
collections = {}

# Load employee data from CSV
def load_employee_data(file_name='Employee_data.csv'):
    try:
        df = pd.read_csv(file_name, encoding='ISO-8859-1')
        return df.to_dict('records')
    except FileNotFoundError:
        print("CSV file not found.")
        return []

# Function to create a collection
def createCollection(p_collection_name, file_name='Employee_data.csv'):
    employees = load_employee_data(file_name)
    collections[p_collection_name] = employees
    return f"Collection '{p_collection_name}' created successfully."

# Function to index data, excluding a specific column
def indexData(p_collection_name, p_exclude_column):
    collection = collections.get(p_collection_name, [])
    indexed_data = [{k: v for k, v in emp.items() if k != p_exclude_column} for emp in collection]
    collections[p_collection_name] = indexed_data
    return f"Indexed data in '{p_collection_name}', excluding column '{p_exclude_column}'."

# Function to search by column
def searchByColumn(p_collection_name, p_column_name, p_column_value):
    collection = collections.get(p_collection_name, [])
    results = [emp for emp in collection if emp.get(p_column_name) == p_column_value]
    return results

# Function to get employee count
def getEmpCount(p_collection_name):
    collection = collections.get(p_collection_name, [])
    return len(collection)

# Function to delete employee by ID
def delEmpById(p_collection_name, p_employee_id):
    collection = collections.get(p_collection_name, [])
    collections[p_collection_name] = [emp for emp in collection if emp.get('ID') != p_employee_id]
    return f"Employee with ID {p_employee_id} deleted from '{p_collection_name}'."

# Function to get department facet (employee count per department)
def getDepFacet(p_collection_name):
    collection = collections.get(p_collection_name, [])
    dept_count = {}
    for emp in collection:
        dept = emp.get('Department')
        if dept:
            dept_count[dept] = dept_count.get(dept, 0) + 1
    return dept_count


# Routes for Flask app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_collection():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        createCollection(collection_name)
        return redirect(url_for('index'))
    return render_template('create_collection.html')

@app.route('/index_data', methods=['GET', 'POST'])
def index_data():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        exclude_column = request.form['exclude_column']
        indexData(collection_name, exclude_column)
        return redirect(url_for('index'))
    return render_template('index_data.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        column_name = request.form['column_name']
        column_value = request.form['column_value']
        results = searchByColumn(collection_name, column_name, column_value)
        return render_template('results.html', results=results)
    return render_template('search.html')

@app.route('/facet', methods=['GET', 'POST'])
def facets():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        facets = getDepFacet(collection_name)
        return render_template('facets.html', facets=facets)
    return render_template('facets.html')

# New route to delete an employee by ID
@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        employee_id = request.form['employee_id']
        message = delEmpById(collection_name, employee_id)
        return render_template('delete_employee.html', message=message)
    return render_template('delete_employee.html')

# New route to get employee count in a collection
@app.route('/employee_count', methods=['GET', 'POST'])
def employee_count():
    if request.method == 'POST':
        collection_name = request.form['collection_name']
        count = getEmpCount(collection_name)
        return render_template('employee_count.html', count=count)
    return render_template('employee_count.html')


if __name__ == '__main__':
    app.run(debug=True)
