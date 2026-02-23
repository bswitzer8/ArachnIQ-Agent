from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="ArachnIQ-Agent Hackathon Mock API")

# Simple In-memory store
users = []
products = [
    {"id": 1, "name": "Gemini Ultra Lens", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Neural Link Pro", "price": 2499.00, "stock": 5},
    {"id": 3, "name": "AI Debugger Stick", "price": 49.99, "stock": 100},
]
cart = []

class User(BaseModel):
    username: str
    email: str

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the ArachnIQ-Agent Mock API", "status": "online"}

@app.post("/users/register")
def register_user(user: User):
    # BUG: No validation if user already exists
    # BUG: No email format validation (FastAPI/Pydantic would do some, but we'll keep it simple)
    users.append(user.dict())
    return {"message": "User registered successfully", "user": user}

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    # BUG: Crashes if product_id is 999 instead of 404
    if product_id == 999:
        raise Exception("Internal Server Error Simulator")
    
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/cart/add")
def add_to_cart(item: CartItem):
    # BUG: Doesn't check if product_id exists
    # BUG: Allows negative quantity
    if item.quantity == 0:
        # Inconsistent return type/status
        return {"error": "Quantity cannot be zero"}, 400
    
    cart.append(item.dict())
    return {"message": "Added to cart", "cart_size": len(cart)}

@app.post("/checkout")
def checkout():
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # BUG: Race condition simulator (not really, but just a logic bug)
    # Always fails if more than 5 items in cart
    if len(cart) > 5:
        return {"status": "failure", "reason": "Too many items for this demo API"}
    
    total = sum(next((p["price"] for p in products if p["id"] == i["product_id"]), 0) * i["quantity"] for i in cart)
    cart.clear()
    return {"status": "success", "total": total}
