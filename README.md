# ganeshNeo4j-interview
neo4j assignment 
GET API URl - http://localhost:8080/api 

POST API - http://localhost:8080/api


Sample body employee creation  
-----------------------------------------

{
  "operation": "create_employee",
  "node_type": "Employee",
  "data": [
    {
      "name": "emp1",
      "emp_id": 1,
      "email": "abc@123"
    },
    {
      "name": "emp2",
      "emp_id": 2,
      "email": "abc@123"
    }
  ]
}



Sample body address creation  

--------------------------------------------
{
  "operation": "create_address",
  "node_type": "Address",
  "data": [
    {
      "emp_id": 5,
      "street": "123 Main St",
      "city": "City",
      "state": "State",
      "country": "Country"
    },
    {
      "emp_id": 5555,
      "street": "123 Main St",
      "city": "City",
      "state": "State",
      "country": "Country",
      "pincode":32112
    }
    
  ]
}
-----------------------------------------------------------