# neo4j_operations.py

from neo4j import GraphDatabase

# neo4j_operations.py

from neo4j_credentials import neo4j_uri, neo4j_username, neo4j_password


def merge_or_create_employee(emp_id, **kwargs):
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    with driver.session() as session:
        merge_query = (
            f"MATCH (e:Employee {{emp_id: $emp_id}}) "
            "SET e += $props "
            "RETURN e"
        )
        result = session.run(merge_query, emp_id=emp_id, props=kwargs)
        return result.single()

def create_node(label, emp_id=None, **kwargs):
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    with driver.session() as session:
        if emp_id is not None:
            kwargs['emp_id'] = emp_id
        cypher_query = f"CREATE (n:{label} {{{', '.join([f'{key}: ${key}' for key in kwargs.keys()])}}})"
        print("Cypher Query:", cypher_query)  # Print the Cypher query
        session.run(cypher_query, **kwargs)


def create_relationship(emp_id):
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    with driver.session() as session:
        # Check if the relationship already exists
        relationship_check_query = (
            "MATCH (e:Employee {emp_id: $emp_id})-[:HAS_ADDRESS]->(a:Address {emp_id: $emp_id}) "
            "RETURN COUNT(*) AS count"
        )
        result = session.run(relationship_check_query, emp_id=emp_id)
        print("raltionship count" ,result)
        count = result.single().get('count', 0)
        
        # If the relationship doesn't exist, create it
        if count == 0:
            relationship_query = (
                "MATCH (e:Employee {emp_id: $emp_id}), (a:Address {emp_id: $emp_id}) "
                "MERGE (e)-[:HAS_ADDRESS]->(a)"
            )
            session.run(relationship_query, emp_id=emp_id)
            print("Relationship created successfully for emp_id:", emp_id)
        else:
            print("Relationship already exists for emp_id:", emp_id)


#  def get_all_employees_with_addresses():
#     driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
#     with driver.session() as session:
#         result = session.run("MATCH (e:Employee) optional match (a:Address) where a.emp_id=e.emp_id    RETURN e, a")
#         employees_with_addresses = [(record['e'], record['a']) for record in result]
#         return employees_with_addresses 
        
def get_all_employees_with_addresses():
    try:
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
        with driver.session() as session:
            result = session.run("MATCH (e:Employee) OPTIONAL MATCH (a:Address) WHERE a.emp_id = e.emp_id RETURN e, a")

            if result is None:
                return {"employees_with_addresses": []}  # Return an empty list if no records are found

            employees_with_addresses = []
            for record in result:
                employee_dict = dict(record['e'])
                address_dict = dict(record['a']) if record['a'] is not None else None
                employees_with_addresses.append({'employee': employee_dict, 'address': address_dict})

            print("Contents of employees_with_addresses:", employees_with_addresses)  # Print out the contents for debugging

            return {"formatted_data": employees_with_addresses}
    except Exception as e:
        print("Error in get_all_employees_with_addresses:", e)
        return {"errorMessage": str(e)}  # Return an error message if any exception occurs






        

# def get_all_employees_with_addresses():
#     try:
#         driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
#         with driver.session() as session:
#             result = session.run("MATCH (e:Employee) OPTIONAL MATCH (a:Address) WHERE a.emp_id = e.emp_id RETURN e, a")

#             if result is None:
#                 return {"employees_with_addresses": []}  # Return an empty list if no records are found

#             formatted_data = []
#             for record in result:
#                 employee = record['e']
#                 address = record['a']
#                 if employee is not None:
#                     employee_dict = dict(employee)
#                     address_dict = dict(address) if address is not None else None
#                     formatted_data.append({'employee': employee_dict, 'address': address_dict})

#             return {"employees_with_addresses": formatted_data}
#     except Exception as e:
#         print("Error in get_all_employees_with_addresses:", e)
#         return {"errorMessage": str(e)}  # Return an error message if any exception occurs





