"""
IKEA Furniture API
-----------------
A FastAPI application that provides CRUD operations for IKEA furniture items.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date

# Import our models from ikea_furniture.py
from ikea_furniture import (
    engine, IkeaSofa, IkeaDiningTable, IkeaMatress, ShoppingCart, CartItem,
    create_tables, create_sample_data
)
import json

# Create FastAPI app
app = FastAPI(
    title="IKEA Furniture API",
    description="API for managing IKEA furniture inventory",
    version="1.0.0"
)

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session


# --- Startup Event ---
@app.on_event("startup")
async def on_startup():
    """Initialize database on startup if needed"""
    create_tables()
    # Uncomment the line below if you want to create sample data on startup
    # create_sample_data()


# --- Sofa CRUD Operations ---
@app.post("/sofas/", response_model=IkeaSofa, tags=["Sofas"])
def create_sofa(sofa: IkeaSofa, session: Session = Depends(get_session)):
    """Create a new sofa"""
    session.add(sofa)
    session.commit()
    session.refresh(sofa)
    return sofa


@app.get("/sofas/", response_model=List[IkeaSofa], tags=["Sofas"])
def read_sofas(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    material: Optional[str] = Query(None, description="Filter by material"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    has_sleeper: Optional[bool] = Query(None, description="Filter by sleeper feature")
):
    """Get all sofas with optional filtering"""
    query = select(IkeaSofa)
    
    # Apply filters if provided
    if material:
        query = query.where(IkeaSofa.material == material)
    if min_price is not None:
        query = query.where(IkeaSofa.price >= min_price)
    if max_price is not None:
        query = query.where(IkeaSofa.price <= max_price)
    if has_sleeper is not None:
        query = query.where(IkeaSofa.has_sleeper == has_sleeper)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()


@app.get("/sofas/{sofa_id}", response_model=IkeaSofa, tags=["Sofas"])
def read_sofa(sofa_id: int, session: Session = Depends(get_session)):
    """Get a specific sofa by ID"""
    sofa = session.get(IkeaSofa, sofa_id)
    if not sofa:
        raise HTTPException(status_code=404, detail="Sofa not found")
    return sofa


@app.put("/sofas/{sofa_id}", response_model=IkeaSofa, tags=["Sofas"])
def update_sofa(sofa_id: int, sofa_data: IkeaSofa, session: Session = Depends(get_session)):
    """Update a sofa"""
    db_sofa = session.get(IkeaSofa, sofa_id)
    if not db_sofa:
        raise HTTPException(status_code=404, detail="Sofa not found")
    
    # Update the sofa attributes
    sofa_data_dict = sofa_data.dict(exclude_unset=True)
    for key, value in sofa_data_dict.items():
        setattr(db_sofa, key, value)
    
    session.add(db_sofa)
    session.commit()
    session.refresh(db_sofa)
    return db_sofa


@app.delete("/sofas/{sofa_id}", tags=["Sofas"])
def delete_sofa(sofa_id: int, session: Session = Depends(get_session)):
    """Delete a sofa"""
    sofa = session.get(IkeaSofa, sofa_id)
    if not sofa:
        raise HTTPException(status_code=404, detail="Sofa not found")
    
    session.delete(sofa)
    session.commit()
    return {"message": f"Sofa with ID {sofa_id} deleted successfully"}


# --- Dining Table CRUD Operations ---
@app.post("/dining-tables/", response_model=IkeaDiningTable, tags=["Dining Tables"])
def create_dining_table(table: IkeaDiningTable, session: Session = Depends(get_session)):
    """Create a new dining table"""
    session.add(table)
    session.commit()
    session.refresh(table)
    return table


@app.get("/dining-tables/", response_model=List[IkeaDiningTable], tags=["Dining Tables"])
def read_dining_tables(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    material: Optional[str] = Query(None, description="Filter by material"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    shape: Optional[str] = Query(None, description="Filter by table shape"),
    extendable: Optional[bool] = Query(None, description="Filter by extendable feature")
):
    """Get all dining tables with optional filtering"""
    query = select(IkeaDiningTable)
    
    # Apply filters if provided
    if material:
        query = query.where(IkeaDiningTable.material == material)
    if min_price is not None:
        query = query.where(IkeaDiningTable.price >= min_price)
    if max_price is not None:
        query = query.where(IkeaDiningTable.price <= max_price)
    if shape:
        query = query.where(IkeaDiningTable.shape == shape)
    if extendable is not None:
        query = query.where(IkeaDiningTable.extendable == extendable)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()


@app.get("/dining-tables/{table_id}", response_model=IkeaDiningTable, tags=["Dining Tables"])
def read_dining_table(table_id: int, session: Session = Depends(get_session)):
    """Get a specific dining table by ID"""
    table = session.get(IkeaDiningTable, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Dining table not found")
    return table


@app.put("/dining-tables/{table_id}", response_model=IkeaDiningTable, tags=["Dining Tables"])
def update_dining_table(table_id: int, table_data: IkeaDiningTable, session: Session = Depends(get_session)):
    """Update a dining table"""
    db_table = session.get(IkeaDiningTable, table_id)
    if not db_table:
        raise HTTPException(status_code=404, detail="Dining table not found")
    
    # Update the table attributes
    table_data_dict = table_data.dict(exclude_unset=True)
    for key, value in table_data_dict.items():
        setattr(db_table, key, value)
    
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    return db_table


@app.delete("/dining-tables/{table_id}", tags=["Dining Tables"])
def delete_dining_table(table_id: int, session: Session = Depends(get_session)):
    """Delete a dining table"""
    table = session.get(IkeaDiningTable, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Dining table not found")
    
    session.delete(table)
    session.commit()
    return {"message": f"Dining table with ID {table_id} deleted successfully"}


# --- Mattress CRUD Operations ---
@app.post("/mattresses/", response_model=IkeaMatress, tags=["Mattresses"])
def create_mattress(mattress: IkeaMatress, session: Session = Depends(get_session)):
    """Create a new mattress"""
    session.add(mattress)
    session.commit()
    session.refresh(mattress)
    return mattress


@app.get("/mattresses/", response_model=List[IkeaMatress], tags=["Mattresses"])
def read_mattresses(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    material: Optional[str] = Query(None, description="Filter by material"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    size: Optional[str] = Query(None, description="Filter by mattress size"),
    firmness: Optional[str] = Query(None, description="Filter by firmness level")
):
    """Get all mattresses with optional filtering"""
    query = select(IkeaMatress)
    
    # Apply filters if provided
    if material:
        query = query.where(IkeaMatress.material == material)
    if min_price is not None:
        query = query.where(IkeaMatress.price >= min_price)
    if max_price is not None:
        query = query.where(IkeaMatress.price <= max_price)
    if size:
        query = query.where(IkeaMatress.size == size)
    if firmness:
        query = query.where(IkeaMatress.firmness == firmness)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()


@app.get("/mattresses/{mattress_id}", response_model=IkeaMatress, tags=["Mattresses"])
def read_mattress(mattress_id: int, session: Session = Depends(get_session)):
    """Get a specific mattress by ID"""
    mattress = session.get(IkeaMatress, mattress_id)
    if not mattress:
        raise HTTPException(status_code=404, detail="Mattress not found")
    return mattress


@app.put("/mattresses/{mattress_id}", response_model=IkeaMatress, tags=["Mattresses"])
def update_mattress(mattress_id: int, mattress_data: IkeaMatress, session: Session = Depends(get_session)):
    """Update a mattress"""
    db_mattress = session.get(IkeaMatress, mattress_id)
    if not db_mattress:
        raise HTTPException(status_code=404, detail="Mattress not found")
    
    # Update the mattress attributes
    mattress_data_dict = mattress_data.dict(exclude_unset=True)
    for key, value in mattress_data_dict.items():
        setattr(db_mattress, key, value)
    
    session.add(db_mattress)
    session.commit()
    session.refresh(db_mattress)
    return db_mattress


@app.delete("/mattresses/{mattress_id}", tags=["Mattresses"])
def delete_mattress(mattress_id: int, session: Session = Depends(get_session)):
    """Delete a mattress"""
    mattress = session.get(IkeaMatress, mattress_id)
    if not mattress:
        raise HTTPException(status_code=404, detail="Mattress not found")
    
    session.delete(mattress)
    session.commit()
    return {"message": f"Mattress with ID {mattress_id} deleted successfully"}


# --- Shopping Cart CRUD Operations ---
@app.post("/carts/", response_model=ShoppingCart, tags=["Shopping Carts"])
def create_cart(cart: ShoppingCart, session: Session = Depends(get_session)):
    """Create a new shopping cart"""
    session.add(cart)
    session.commit()
    session.refresh(cart)
    return cart


@app.get("/carts/", response_model=List[ShoppingCart], tags=["Shopping Carts"])
def read_carts(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    customer_name: Optional[str] = Query(None, description="Filter by customer name")
):
    """Get all shopping carts with optional filtering"""
    query = select(ShoppingCart)
    
    # Apply filters if provided
    if customer_name:
        query = query.where(ShoppingCart.customer_name.contains(customer_name))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()


@app.get("/carts/{cart_id}", response_model=ShoppingCart, tags=["Shopping Carts"])
def read_cart(cart_id: int, session: Session = Depends(get_session)):
    """Get a specific shopping cart by ID"""
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return cart


@app.put("/carts/{cart_id}", response_model=ShoppingCart, tags=["Shopping Carts"])
def update_cart(cart_id: int, cart_data: ShoppingCart, session: Session = Depends(get_session)):
    """Update a shopping cart's basic information (customer details)"""
    db_cart = session.get(ShoppingCart, cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Update only the customer information
    if cart_data.customer_name is not None:
        db_cart.customer_name = cart_data.customer_name
    if cart_data.customer_email is not None:
        db_cart.customer_email = cart_data.customer_email
    
    session.add(db_cart)
    session.commit()
    session.refresh(db_cart)
    return db_cart


@app.delete("/carts/{cart_id}", tags=["Shopping Carts"])
def delete_cart(cart_id: int, session: Session = Depends(get_session)):
    """Delete a shopping cart"""
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Also delete all cart items (they will be orphaned otherwise)
    cart_items = session.exec(select(CartItem).where(CartItem.cart_id == cart_id)).all()
    for item in cart_items:
        session.delete(item)
    
    session.delete(cart)
    session.commit()
    return {"message": f"Shopping cart with ID {cart_id} deleted successfully"}


# --- Cart Items Operations ---
@app.post("/carts/{cart_id}/items", tags=["Shopping Carts"])
def add_item_to_cart(cart_id: int, furniture_type: str, furniture_id: int, quantity: int = 1, session: Session = Depends(get_session)):
    """Add an item to a shopping cart"""
    # Check if cart exists
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Check if furniture exists and get the right type
    furniture = None
    if furniture_type == "sofa":
        furniture = session.get(IkeaSofa, furniture_id)
    elif furniture_type == "dining_table":
        furniture = session.get(IkeaDiningTable, furniture_id)
    elif furniture_type == "matress":
        furniture = session.get(IkeaMatress, furniture_id)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid furniture type: {furniture_type}")
    
    if not furniture:
        raise HTTPException(status_code=404, detail=f"{furniture_type.capitalize()} with ID {furniture_id} not found")
    
    # Add item to cart
    cart_item = cart.add_item(session, furniture, quantity)
    
    # Return the added item details
    furniture_dict = json.loads(cart_item.furniture_data)
    return {
        "id": cart_item.id,
        "furniture_type": cart_item.furniture_type,
        "furniture_id": cart_item.furniture_id,
        "quantity": cart_item.quantity,
        "name": furniture_dict.get("name", "Unknown"),
        "price": furniture_dict.get("price", 0.0),
        "subtotal": furniture_dict.get("price", 0.0) * cart_item.quantity
    }


@app.get("/carts/{cart_id}/items", tags=["Shopping Carts"])
def get_cart_items(cart_id: int, session: Session = Depends(get_session)):
    """Get all items in a shopping cart"""
    # Check if cart exists
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Get cart summary
    summary = cart.get_cart_summary(session)
    return summary


@app.put("/carts/{cart_id}/items/{item_id}", tags=["Shopping Carts"])
def update_cart_item(cart_id: int, item_id: int, quantity: int, session: Session = Depends(get_session)):
    """Update the quantity of an item in the cart"""
    # Check if cart exists
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Check if item exists and belongs to this cart
    item = session.get(CartItem, item_id)
    if not item or item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Update quantity
    item.quantity = quantity
    session.add(item)
    session.commit()
    session.refresh(item)
    
    # Return updated item details
    furniture_dict = json.loads(item.furniture_data)
    return {
        "id": item.id,
        "furniture_type": item.furniture_type,
        "furniture_id": item.furniture_id,
        "quantity": item.quantity,
        "name": furniture_dict.get("name", "Unknown"),
        "price": furniture_dict.get("price", 0.0),
        "subtotal": furniture_dict.get("price", 0.0) * item.quantity
    }


@app.delete("/carts/{cart_id}/items/{item_id}", tags=["Shopping Carts"])
def remove_cart_item(cart_id: int, item_id: int, session: Session = Depends(get_session)):
    """Remove an item from the cart"""
    # Check if cart exists
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Check if item exists and belongs to this cart
    item = session.get(CartItem, item_id)
    if not item or item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Delete the item
    session.delete(item)
    session.commit()
    
    return {"message": f"Item removed from cart successfully"}


@app.get("/carts/{cart_id}/total", tags=["Shopping Carts"])
def get_cart_total(cart_id: int, session: Session = Depends(get_session)):
    """Get the total price and quantity of items in a cart"""
    # Check if cart exists
    cart = session.get(ShoppingCart, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    
    # Calculate totals
    total_price = cart.calculate_total_price(session)
    total_quantity = cart.calculate_total_quantity(session)
    
    return {
        "cart_id": cart_id,
        "customer_name": cart.customer_name,
        "total_price": total_price,
        "total_quantity": total_quantity
    }


# --- General Endpoints ---
@app.get("/", tags=["General"])
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to the IKEA Furniture API",
        "endpoints": {
            "sofas": "/sofas/",
            "dining_tables": "/dining-tables/",
            "mattresses": "/mattresses/",
            "shopping_carts": "/carts/"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
