from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI(
    title="ArachnIQ-Agent Hackathon Mock API",
    description="A vulnerable API designed for AI-powered testing demonstrations.",
    version="1.0.0"
)

# --- In-Memory Database ---
users_db: List[Dict] = []
products_db: List[Dict] = [
    {"id": 1, "name": "Quantum Processor", "price": 4999.99, "stock": 5},
    {"id": 2, "name": "Neural Interface Headset", "price": 299.00, "stock": 15},
    {"id": 3, "name": "AI Debugging Assistant", "price": 49.99, "stock": 100},
    {"id": 4, "name": "Holographic Display", "price": 899.50, "stock": 8},
]
cart_db: List[Dict] = []

# --- Models ---
class User(BaseModel):
    username: str
    email: str

class CartItem(BaseModel):
    product_id: int
    quantity: int

# --- Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """Welcome endpoint to check API status."""
    return {"message": "Welcome to the ArachnIQ-Agent Mock API", "status": "online"}

@app.post("/users/register", tags=["User Management"])
def register_user(user: User):
    """
    Register a new user.
    BUG: Intentionally does not validate if the user already exists.
    BUG: Intentionally does not validate email format.
    """
    # Intentional BUG: No duplicate check
    users_db.append(user.model_dump())
    return {"message": "User registered successfully", "user": user}

@app.get("/users", tags=["User Management"])
def get_users():
    """List all registered users."""
    return users_db

@app.get("/products", tags=["Products"])
def get_products():
    """List all available products."""
    return products_db

@app.get("/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    """
    Get product details by ID.
    BUG: Crashes with a 500 error if product_id is 999.
    """
    # Intentional BUG: Simulation of an unhandled exception
    if product_id == 999:
        raise Exception("Internal Server Error Simulator: Unhandled Logic Exception")

    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/cart/add", tags=["Cart"])
def add_to_cart(item: CartItem):
    """
    Add an item to the cart.
    BUG: Does not validate if product_id exists in products_db.
    BUG: Allows adding 0 or negative quantities.
    """
    # Intentional BUG: Allows 0 or negative quantity
    # It returns a 400 for 0, but allows negative numbers to pass through
    if item.quantity == 0:
        # Inconsistent error response format
        return {"error": "Quantity cannot be zero"}, 400

    # Intentional BUG: No product existence check

    cart_db.append(item.model_dump())
    return {"message": "Added to cart", "cart_size": len(cart_db)}

@app.get("/cart", tags=["Cart"])
def view_cart():
    """View current cart contents."""
    return cart_db

@app.post("/cart/checkout", tags=["Cart"])
def checkout():
    """
    Process checkout.
    BUG: Fails artificially if the cart has more than 5 items.
    """
    if not cart_db:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Intentional BUG: "Race condition" simulator / logic error
    if len(cart_db) > 5:
        return {"status": "failure", "reason": "System overload: Too many items in cart for this demo."}

    # Calculate total
    total = 0.0
    for item in cart_db:
        # If product doesn't exist (due to previous bug), this price lookup might fail or default to 0
        product = next((p for p in products_db if p["id"] == item["product_id"]), None)
        price = product["price"] if product else 0.0
        total += price * item["quantity"]

    cart_db.clear()
    return {"status": "success", "total_amount": round(total, 2), "message": "Order processed successfully"}

@app.delete("/cart/clear", tags=["Cart"])
def clear_cart():
    """Empty the cart."""
    cart_db.clear()
    return {"message": "Cart cleared"}
