from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from mysql.connector import (connection)
import os

class DBModel(BaseModel):
    name: str
    department: str

db = connection.MySQLConnection(host = os.environ['DB_HOSTNAME'], user = os.environ['DB_USERNAME'], password = os.environ['DB_PASSWORD'], database = os.environ['DB_NAME']) # outlined in docker-compose.yml
cursor = db.cursor()
app = FastAPI()

# Root GET
@app.get("/")
def get_root():
    return {"message": "Hello World"}

# Create/add an employee
@app.post("/employees", status_code=status.HTTP_201_CREATED)
def insert_employee(employee: DBModel):
    insert_query = """INSERT INTO employees (name, department) VALUES (%s, %s)"""
    values = (employee.name, employee.department)
    try:
        cursor.execute(insert_query, values)
        db.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Employee insertion failed: {err}")

    return {"message": "Employee insertion successful."}

# Retrieve all employees
@app.get("/employees", status_code=status.HTTP_200_OK)
def get_employees():
    select_query = "SELECT * FROM employees"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results
    
# Retrieve a specific employee by ID
@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee(employee_id: int):
    select_query = "SELECT * FROM employees WHERE id = %s"
    cursor.execute(select_query, (employee_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Employee not found.")

# Update an existing employee
@app.put("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def update_employee(employee_id: int, employee: DBModel):
    update_query = """UPDATE employees SET name = %s, department = %s WHERE id = %s"""
    values = (employee.name, employee.department, employee_id)

    cursor.execute(update_query, values)
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return {"message": "Employee updated successfully."}

# Delete an employee
@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(employee_id: int):
    delete_query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(delete_query, (employee_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return {"message": "Employee deleted successfully."}
