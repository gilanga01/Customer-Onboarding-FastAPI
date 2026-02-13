# Import necessary libraries
from fastapi import FastAPI, HTTPException  # FastAPI framework and exception handling
from pydantic import BaseModel, EmailStr    # BaseModel for data validation, EmailStr for email validation
from typing import List                      # List type hint
from uuid import uuid4                        # To generate unique IDs for each customer

# Create the FastAPI app instance
app = FastAPI()

# -----------------------------
# In-memory storage (temporary database)
# -----------------------------
# This list will store all customer data while the server is running
# Note: Data will be lost if you restart the server
onboarding_data = []

# -----------------------------
# Data Models
# -----------------------------
# Models define the structure and type of data our API expects

# Model for incoming customer data
class Customer(BaseModel):
    name: str           # Customer's name (string)
    email: EmailStr     # Customer's email (validated automatically)
    phone: str          # Customer's phone number

# Model for responses that include an ID
class CustomerResponse(Customer):
    id: str             # Unique identifier for each customer

# -----------------------------
# API Routes (Endpoints)
# -----------------------------

# Root endpoint (just a welcome message)
@app.get("/")
def index():
    return {"message": "Welcome to the Customer Onboarding API!"}

# -----------------------------
# CREATE Customer
# -----------------------------
@app.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(customer: Customer):
    """
    Add a new customer to the onboarding_data list.
    - `customer` is automatically validated by Pydantic.
    - A unique ID is generated for each customer using uuid4().
    """
    customer_dict = customer.dict()  # Convert Pydantic model to a dictionary
    customer_dict["id"] = str(uuid4())  # Add unique ID
    onboarding_data.append(customer_dict)  # Save customer to in-memory storage
    return customer_dict  # Return the created customer data

# -----------------------------
# READ ALL Customers
# -----------------------------
@app.get("/customers", response_model=List[CustomerResponse])
def get_customers():
    """
    Retrieve all customers from the onboarding_data list.
    Returns a list of CustomerResponse objects.
    """
    return onboarding_data

# -----------------------------
# READ ONE Customer
# -----------------------------
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    """
    Retrieve a single customer by their ID.
    - If the ID does not exist, return a 404 error.
    """
    for customer in onboarding_data:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

# -----------------------------
# UPDATE Customer
# -----------------------------
@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, updated_customer: Customer):
    """
    Update an existing customer's data by ID.
    - Replace name, email, and phone with new data.
    - If the ID does not exist, return a 404 error.
    """
    for customer in onboarding_data:
        if customer["id"] == customer_id:
            customer["name"] = updated_customer.name
            customer["email"] = updated_customer.email
            customer["phone"] = updated_customer.phone
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

# -----------------------------
# DELETE Customer
# -----------------------------
@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: str):
    """
    Delete a customer from the onboarding_data list by ID.
    - Returns 204 No Content on success.
    - If the ID does not exist, return a 404 error.
    """
    for index, customer in enumerate(onboarding_data):
        if customer["id"] == customer_id:
            onboarding_data.pop(index)  # Remove the customer from the list
            return
    raise HTTPException(status_code=404, detail="Customer not found")
