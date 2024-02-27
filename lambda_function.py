from flask import Flask, request, jsonify
import json
import logging
from neo4j_operations import merge_or_create_employee, create_node, create_relationship, get_all_employees_with_addresses

app = Flask(__name__)

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route('/api', methods=['POST', 'GET'])
def lambda_handler():
    if request.method == 'POST':
        event = request.get_json()
        operation = event.get('operation', 'get_all_employees')
        print("Operation:", operation)  # Debugging statement

        if operation == 'create_employee':
            node_type = event.get('node_type')
            employee_data_list = event.get('data', [])
            for employee_data in employee_data_list:
                emp_id = employee_data.get('emp_id')  # Extract emp_id
                if emp_id:
                    del employee_data['emp_id']  # Remove emp_id from data
                    existing_employee = merge_or_create_employee(emp_id, **employee_data)  # Pass data without emp_id
                    if existing_employee:
                        print("Employee updated successfully:", existing_employee)
                    else:
                        create_node(node_type, emp_id=emp_id, **employee_data)  # Create employee node with emp_id
                        print("Employee created successfully:", employee_data)
                else:
                    print("Employee ID not provided for data:", employee_data)

            # Return a response
            return jsonify({'message': 'Employee creation/update successful'}), 200

        elif operation == 'create_address':
            node_type = event.get('node_type')
            address_data_list = event.get('data', [])
            for address_data in address_data_list:
                emp_id = address_data.get('emp_id')  # Extract emp_id
                if emp_id:
                    del address_data['emp_id']  # Remove emp_id from data
                    create_node(node_type, emp_id=emp_id, **address_data)  # Create address node without emp_id
                    create_relationship(emp_id)  # Create relationship between employee and address
                    print("Address created successfully:", address_data)
                else:
                    print("Employee ID not provided for address data:", address_data)

            # Return a response
            return jsonify({'message': 'Address creation successful'}), 200

        else:
            print("Invalid operation:", operation)  # Debugging statement
            return jsonify({'message': 'Invalid operation'}), 400

    elif request.method == 'GET':
        response = get_all_employees_with_addresses()  # Fetch the data
        if 'formatted_data' in response:
            formatted_data = response['formatted_data']
        else:
            formatted_data = []  # Set default empty list if key is missing

        return jsonify({'employees_with_addresses': formatted_data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
