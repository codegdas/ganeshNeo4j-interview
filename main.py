from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

uri = "bolt://54.196.82.220:7687"
# Neo4j connection details
username = "neo4j"
password = "AdminGanesh"

# Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))


# Create an Employee node in Neo4j
def create_employee(name, emp_id):
    with driver.session() as session:
        session.run('CREATE (:Employee {name: $name, emp_id: $emp_id})', name=name, emp_id=emp_id)


# Return all Employee nodes from Neo4j
def get_all_employees():
    with driver.session() as session:
        result = session.run("MATCH (e:Employee) RETURN e")
        employees = [dict(record['e']) for record in result]
        return employees


@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get('name')
    emp_id = data.get('emp_id')
    create_employee(name, emp_id)
    return jsonify({'message': 'Employee created '}), 201


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = get_all_employees()
    return jsonify({'employees': employees}), 200


if __name__ == '__main__':
    app.run(debug=True)
