# Import necessary libraries
from fastapi import FastAPI, HTTPException  # FastAPI framework and exception handling
from pydantic import BaseModel, EmailStr    # BaseModel for data validation, EmailStr for email validation
from typing import List                      # List type hint

# Create the FastAPI app instance
app = FastAPI()

# -----------------------------
# In-memory storage (temporary database)
# -----------------------------
# This list will store all customer data while the server is running
# Note: Data will be lost if you restart the server
onboarding_data = []
next_id = 1  # Auto-increment ID counter

# -----------------------------
# Data Models
# -----------------------------

# Model for incoming customer data
class Customer(BaseModel):
    name: str
    email: EmailStr
    phone: str

# Model for responses that include an ID
class CustomerResponse(Customer):
    id: str  # 4-digit ID


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
    global next_id

    customer_dict = customer.dict()
    customer_dict["id"] = f"{next_id:04d}"  # Format ID as 4 digits (0001, 0002...)
    next_id += 1

    onboarding_data.append(customer_dict)
    return customer_dict


# -----------------------------
# READ ALL Customers
# -----------------------------
@app.get("/customers", response_model=List[CustomerResponse])
def get_customers():
    return onboarding_data


# -----------------------------
# READ ONE Customer
# -----------------------------
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    for customer in onboarding_data:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")


# -----------------------------
# UPDATE Customer
# -----------------------------
@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, updated_customer: Customer):
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
    for index, customer in enumerate(onboarding_data):
        if customer["id"] == customer_id:
            onboarding_data.pop(index)
            return
    raise HTTPException(status_code=404, detail="Customer not found")
