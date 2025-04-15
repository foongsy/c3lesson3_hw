import streamlit as st
import requests
import json
from typing import Dict, List, Optional

# Constants
API_BASE_URL = "http://localhost:8000"

# Set page config
st.set_page_config(
    page_title="IKEA Furniture Store",
    page_icon="🪑",
    layout="wide"
)

# Helper functions
def make_api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict] = None,
    params: Optional[Dict] = None
) -> Dict:
    """Make API requests with error handling"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json() if response.text else {}
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {}

# Sidebar navigation
st.sidebar.title("IKEA Furniture Store")
page = st.sidebar.selectbox(
    "Navigation",
    ["Sofas", "Dining Tables", "Mattresses", "Shopping Cart"]
)

# Sofas Page
if page == "Sofas":
    st.title("🛋️ Sofas")
    
    tab1, tab2, tab3 = st.tabs(["Browse Sofas", "Add New Sofa", "Edit/Delete Sofa"])
    
    with tab1:
        st.subheader("Browse Sofas")
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            material = st.text_input("Material")
        with col2:
            min_price = st.number_input("Min Price", min_value=0.0)
        with col3:
            max_price = st.number_input("Max Price", min_value=0.0)
        has_sleeper = st.checkbox("Has Sleeper")
        
        # Get sofas with filters
        params = {
            "material": material if material else None,
            "min_price": min_price if min_price > 0 else None,
            "max_price": max_price if max_price > 0 else None,
            "has_sleeper": has_sleeper
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        sofas = make_api_request("/sofas/", params=params)
        if sofas:
            for sofa in sofas:
                with st.expander(f"{sofa.get('name', 'Unnamed Sofa')} - ${sofa.get('price', 0.0)}"):
                    st.write(f"Material: {sofa.get('material', 'Not specified')}")
                    st.write(f"Color: {sofa.get('color', 'Not specified')}")
                    st.write(f"Has Sleeper: {'Yes' if sofa.get('has_sleeper', False) else 'No'}")
    
    with tab2:
        st.subheader("Add New Sofa")
        with st.form("add_sofa_form"):
            name = st.text_input("Name")
            price = st.number_input("Price", min_value=0.0)
            material = st.text_input("Material")
            color = st.text_input("Color")
            has_sleeper = st.checkbox("Has Sleeper Feature")
            
            if st.form_submit_button("Add Sofa"):
                sofa_data = {
                    "name": name,
                    "price": price,
                    "material": material,
                    "color": color,
                    "has_sleeper": has_sleeper
                }
                response = make_api_request("/sofas/", method="POST", data=sofa_data)
                if response:
                    st.success("Sofa added successfully!")

    with tab3:
        st.subheader("Edit/Delete Sofa")
        sofa_id = st.number_input("Enter Sofa ID", min_value=1)
        if st.button("Load Sofa"):
            sofa = make_api_request(f"/sofas/{sofa_id}")
            if sofa:
                with st.form("edit_sofa_form"):
                    name = st.text_input("Name", value=sofa.get("name", ""))
                    price = st.number_input("Price", value=sofa.get("price", 0.0))
                    material = st.text_input("Material", value=sofa.get("material", ""))
                    color = st.text_input("Color", value=sofa.get("color", ""))
                    has_sleeper = st.checkbox("Has Sleeper", value=sofa.get("has_sleeper", False))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Sofa"):
                            updated_data = {
                                "name": name,
                                "price": price,
                                "material": material,
                                "color": color,
                                "has_sleeper": has_sleeper
                            }
                            response = make_api_request(
                                f"/sofas/{sofa_id}",
                                method="PUT",
                                data=updated_data
                            )
                            if response:
                                st.success("Sofa updated successfully!")
                    
                    with col2:
                        if st.form_submit_button("Delete Sofa"):
                            response = make_api_request(f"/sofas/{sofa_id}", method="DELETE")
                            if response:
                                st.success("Sofa deleted successfully!")

# Dining Tables Page
elif page == "Dining Tables":
    st.title("🪑 Dining Tables")
    
    tab1, tab2, tab3 = st.tabs(["Browse Tables", "Add New Table", "Edit/Delete Table"])
    
    with tab1:
        st.subheader("Browse Dining Tables")
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            material = st.text_input("Material")
        with col2:
            min_price = st.number_input("Min Price", min_value=0.0)
        with col3:
            max_price = st.number_input("Max Price", min_value=0.0)
        
        shape = st.selectbox("Shape", ["", "Round", "Rectangle", "Square"])
        extendable = st.checkbox("Extendable")
        
        params = {
            "material": material if material else None,
            "min_price": min_price if min_price > 0 else None,
            "max_price": max_price if max_price > 0 else None,
            "shape": shape if shape else None,
            "extendable": extendable
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        tables = make_api_request("/dining-tables/", params=params)
        if tables:
            for table in tables:
                with st.expander(f"{table.get('name', 'Unnamed Table')} - ${table.get('price', 0.0)}"):
                    st.write(f"Material: {table.get('material', 'Not specified')}")
                    st.write(f"Shape: {table.get('shape', 'Not specified')}")
                    st.write(f"Extendable: {'Yes' if table.get('extendable', False) else 'No'}")

    with tab2:
        st.subheader("Add New Table")
        with st.form("add_table_form"):
            name = st.text_input("Name")
            price = st.number_input("Price", min_value=0.0)
            material = st.text_input("Material")
            shape = st.selectbox("Shape", ["Round", "Rectangle", "Square"])
            extendable = st.checkbox("Extendable")
            
            if st.form_submit_button("Add Table"):
                table_data = {
                    "name": name,
                    "price": price,
                    "material": material,
                    "shape": shape,
                    "extendable": extendable
                }
                response = make_api_request("/dining-tables/", method="POST", data=table_data)
                if response:
                    st.success("Table added successfully!")

    with tab3:
        st.subheader("Edit/Delete Table")
        table_id = st.number_input("Enter Table ID", min_value=1)
        if st.button("Load Table"):
            table = make_api_request(f"/dining-tables/{table_id}")
            if table:
                with st.form("edit_table_form"):
                    name = st.text_input("Name", value=table.get("name", ""))
                    price = st.number_input("Price", value=table.get("price", 0.0))
                    material = st.text_input("Material", value=table.get("material", ""))
                    shape = st.selectbox("Shape", 
                                       ["Round", "Rectangle", "Square"],
                                       index=["Round", "Rectangle", "Square"].index(table.get("shape", "Round")))
                    extendable = st.checkbox("Extendable", value=table.get("extendable", False))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Table"):
                            updated_data = {
                                "name": name,
                                "price": price,
                                "material": material,
                                "shape": shape,
                                "extendable": extendable
                            }
                            response = make_api_request(
                                f"/dining-tables/{table_id}",
                                method="PUT",
                                data=updated_data
                            )
                            if response:
                                st.success("Table updated successfully!")
                    
                    with col2:
                        if st.form_submit_button("Delete Table"):
                            response = make_api_request(f"/dining-tables/{table_id}", method="DELETE")
                            if response:
                                st.success("Table deleted successfully!")

# Mattresses Page
elif page == "Mattresses":
    st.title("🛏️ Mattresses")
    
    tab1, tab2, tab3 = st.tabs(["Browse Mattresses", "Add New Mattress", "Edit/Delete Mattress"])
    
    with tab1:
        st.subheader("Browse Mattresses")
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            material = st.text_input("Material")
        with col2:
            min_price = st.number_input("Min Price", min_value=0.0)
        with col3:
            max_price = st.number_input("Max Price", min_value=0.0)
        
        size = st.selectbox("Size", ["", "Twin", "Full", "Queen", "King"])
        firmness = st.selectbox("Firmness", ["", "Soft", "Medium", "Firm"])
        
        params = {
            "material": material if material else None,
            "min_price": min_price if min_price > 0 else None,
            "max_price": max_price if max_price > 0 else None,
            "size": size if size else None,
            "firmness": firmness if firmness else None
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        mattresses = make_api_request("/mattresses/", params=params)
        if mattresses:
            for mattress in mattresses:
                with st.expander(f"{mattress.get('name', 'Unnamed Mattress')} - ${mattress.get('price', 0.0)}"):
                    st.write(f"Size: {mattress.get('size', 'Not specified')}")
                    st.write(f"Firmness: {mattress.get('firmness', 'Not specified')}")
                    st.write(f"Material: {mattress.get('material', 'Not specified')}")

# Shopping Cart Page
else:
    st.title("🛒 Shopping Cart")
    
    tab1, tab2 = st.tabs(["View Cart", "Create New Cart"])
    
    with tab1:
        cart_id = st.number_input("Enter Cart ID", min_value=1)
        if st.button("Load Cart"):
            cart_items = make_api_request(f"/carts/{cart_id}/items")
            cart_total = make_api_request(f"/carts/{cart_id}/total")
            
            if cart_items and cart_total:
                st.write(f"Customer: {cart_total.get('customer_name', 'Unknown')}")
                st.write(f"Total Items: {cart_total.get('total_quantity', 0)}")
                st.write(f"Total Price: ${cart_total.get('total_price', 0.0):.2f}")
                
                st.subheader("Cart Items")
                for item in cart_items:
                    with st.expander(f"{item.get('name', 'Unknown Item')} - Quantity: {item.get('quantity', 0)}"):
                        st.write(f"Price per unit: ${item.get('price', 0.0):.2f}")
                        st.write(f"Subtotal: ${item.get('subtotal', 0.0):.2f}")
                        if st.button(f"Remove Item {item.get('id', 'Unknown')}", key=f"remove_{item.get('id', 'Unknown')}"):
                            response = make_api_request(
                                f"/carts/{cart_id}/items/{item.get('id', 'Unknown')}",
                                method="DELETE"
                            )
                            if response:
                                st.success("Item removed successfully!")
                                st.rerun()
    
    with tab2:
        st.subheader("Create New Cart")
        with st.form("create_cart_form"):
            customer_name = st.text_input("Customer Name")
            customer_email = st.text_input("Customer Email")
            
            if st.form_submit_button("Create Cart"):
                cart_data = {
                    "customer_name": customer_name,
                    "customer_email": customer_email
                }
                response = make_api_request("/carts/", method="POST", data=cart_data)
                if response:
                    st.success(f"Cart created successfully! Cart ID: {response['id']}")
