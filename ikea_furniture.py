"""
IKEA Furniture Demo
-------------------
This script demonstrates:
1. Python Type Hinting
2. Pydantic v2 (for data validation)
3. SQLModel (for ORM database operations)
"""

# Import necessary libraries
from typing import Optional, List, Dict, Any
from datetime import date
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel
import random
import json

# Create a SQLite database engine
DATABASE_URL = "sqlite:///ikea_furniture.db"
engine = create_engine(DATABASE_URL)

# Define the parent class using Pydantic (without database table)
class IkeaFurniture(BaseModel):
    """Base class for all IKEA furniture items"""
    name: str
    price: float
    color: str
    material: str
    weight_kg: float
    date_added: date = date.today()
    in_stock: bool = True
    
    def __str__(self) -> str:
        return f"{self.name} ({self.color} {self.material}): ${self.price}"


# Define child classes that will be database tables using SQLModel
class IkeaSofa(SQLModel, IkeaFurniture, table=True):
    """IKEA Sofa model that will be stored in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    seats: int
    has_sleeper: bool = False
    fabric_type: str


class IkeaDiningTable(SQLModel, IkeaFurniture, table=True):
    """IKEA Dining Table model that will be stored in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    seats: int
    shape: str
    extendable: bool = False


class IkeaMatress(SQLModel, IkeaFurniture, table=True):
    """IKEA Matress model that will be stored in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    size: str  # e.g., "Twin", "Queen", "King"
    firmness: str  # e.g., "Soft", "Medium", "Firm"
    thickness_cm: float

# Define a simple shopping cart class for beginners
class CartItem(SQLModel, table=True):
    """An item in a shopping cart"""
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="shoppingcart.id")
    
    # Store furniture type, ID, and quantity as simple fields
    furniture_type: str  # "sofa", "dining_table", or "matress"
    furniture_id: int
    quantity: int = 1
    
    # Store a JSON representation of the furniture item
    furniture_data: str  # JSON string of the furniture item


class ShoppingCart(SQLModel, table=True):
    """A simple shopping cart that can contain different types of IKEA furniture"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_date: date = Field(default_factory=date.today)
    customer_name: str
    customer_email: Optional[str] = None
    
    def add_item(self, session: Session, furniture: Any, quantity: int = 1):
        """Add a furniture item to the cart"""
        # Determine furniture type
        furniture_type_map = {
            IkeaSofa: "sofa",
            IkeaDiningTable: "dining_table",
            IkeaMatress: "matress"
        }
        
        furniture_type = furniture_type_map.get(type(furniture))
        if not furniture_type:
            raise ValueError(f"Unsupported furniture type: {type(furniture)}")
        
        # Get the furniture data directly from the database to ensure all fields are loaded
        session.refresh(furniture)
        
        # Convert furniture to dictionary for storage
        furniture_dict = {
            # Common fields for all furniture types
            'id': furniture.id,
            'name': furniture.name,
            'price': furniture.price,
            'color': furniture.color,
            'material': furniture.material,
            'weight_kg': furniture.weight_kg,
            'in_stock': furniture.in_stock,
            'date_added': furniture.date_added.isoformat() if isinstance(furniture.date_added, date) else str(furniture.date_added)
        }
        
        # Add type-specific fields based on furniture type
        if furniture_type == 'sofa':
            type_specific_fields = {
                'seats': furniture.seats,
                'has_sleeper': furniture.has_sleeper,
                'fabric_type': furniture.fabric_type
            }
        elif furniture_type == 'dining_table':
            type_specific_fields = {
                'seats': furniture.seats,
                'shape': furniture.shape,
                'extendable': furniture.extendable
            }
        elif furniture_type == 'matress':
            type_specific_fields = {
                'size': furniture.size,
                'firmness': furniture.firmness,
                'thickness_cm': furniture.thickness_cm
            }
        
        # Update the dictionary with type-specific fields
        furniture_dict.update(type_specific_fields)
        
        # Convert to JSON
        furniture_json = json.dumps(furniture_dict)
        
        # Create cart item
        cart_item = CartItem(
            cart_id=self.id,
            furniture_type=furniture_type,
            furniture_id=furniture.id,
            quantity=quantity,
            furniture_data=furniture_json
        )
        
        session.add(cart_item)
        session.commit()
        return cart_item
    
    def get_items(self, session: Session) -> List[CartItem]:
        """Get all items in the cart"""
        return session.exec(select(CartItem).where(CartItem.cart_id == self.id)).all()
    
    def calculate_total_price(self, session: Session) -> float:
        """Calculate the total price of all items in the cart"""
        items = self.get_items(session)
        return sum(json.loads(item.furniture_data).get("price", 0.0) * item.quantity for item in items)
    
    def calculate_total_quantity(self, session: Session) -> int:
        """Calculate the total number of items in the cart"""
        items = self.get_items(session)
        return sum(item.quantity for item in items)
    
    def get_cart_summary(self, session: Session) -> Dict:
        """Get a summary of the cart contents and totals"""
        items = self.get_items(session)
        item_details = []
        
        for item in items:
            furniture_dict = json.loads(item.furniture_data)
            item_details.append({
                "type": item.furniture_type,
                "name": furniture_dict.get("name", "Unknown"),
                "price": furniture_dict.get("price", 0.0),
                "quantity": item.quantity,
                "subtotal": furniture_dict.get("price", 0.0) * item.quantity
            })
        
        return {
            "customer": {
                "name": self.customer_name,
                "email": self.customer_email
            },
            "items": item_details,
            "total_items": self.calculate_total_quantity(session),
            "total_price": self.calculate_total_price(session)
        }


def create_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def create_sample_data():
    """Create sample data for each furniture type"""
    # Define common attributes for sample data
    sample_data = {
        'sofas': {
            'class': IkeaSofa,
            'name_prefix': "KIVIK",
            'base_price': 499.99,
            'price_increment': 50,
            'price_variation': 20,
            'colors': ["Gray", "Blue", "Beige", "Black", "White"],
            'materials': ["Polyester", "Cotton", "Leather", "Wool", "Linen"],
            'base_weight': 45.5,
            'weight_increment': 2,
            'specific_attrs': {
                'seats': lambda i: 2 + (i % 3),
                'has_sleeper': lambda i: i % 2 == 0,
                'fabric_type': ["Microfiber", "Velvet", "Canvas", "Chenille", "Tweed"]
            }
        },
        'dining_tables': {
            'class': IkeaDiningTable,
            'name_prefix': "EKEDALEN",
            'base_price': 199.99,
            'price_increment': 30,
            'price_variation': 15,
            'colors': ["Oak", "Birch", "Walnut", "White", "Black"],
            'materials': ["Wood", "Particleboard", "Bamboo", "MDF", "Solid Pine"],
            'base_weight': 25.0,
            'weight_increment': 3,
            'specific_attrs': {
                'seats': lambda i: 4 + (i % 4),
                'shape': ["Rectangle", "Round", "Square", "Oval", "Hexagon"],
                'extendable': lambda i: i % 2 == 0
            }
        },
        'matresses': {
            'class': IkeaMatress,
            'name_prefix': "HAUGESUND",
            'base_price': 299.99,
            'price_increment': 40,
            'price_variation': 25,
            'colors': ["White", "Beige", "Gray", "Off-white", "Cream"],
            'materials': ["Memory Foam", "Spring", "Latex", "Hybrid", "Gel"],
            'base_weight': 15.0,
            'weight_increment': 2,
            'specific_attrs': {
                'size': ["Twin", "Full", "Queen", "King", "California King"],
                'firmness': ["Soft", "Medium-soft", "Medium", "Medium-firm", "Firm"],
                'thickness_cm': lambda i: 15.0 + (i * 0.5)
            }
        }
    }
    
    # Create items for each furniture type
    furniture_items = {}
    
    for furniture_type, config in sample_data.items():
        items = []
        for i in range(10):
            # Create common attributes
            attrs = {
                'name': f"{config['name_prefix']} {i}",
                'price': config['base_price'] + (i * config['price_increment']) + random.uniform(-config['price_variation'], config['price_variation']),
                'color': config['colors'][i % len(config['colors'])],
                'material': config['materials'][i % len(config['materials'])],
                'weight_kg': config['base_weight'] + (i * config['weight_increment'])
            }
            
            # Add specific attributes
            for attr_name, attr_value in config['specific_attrs'].items():
                if callable(attr_value):
                    attrs[attr_name] = attr_value(i)
                elif isinstance(attr_value, list):
                    attrs[attr_name] = attr_value[i % len(attr_value)]
                else:
                    attrs[attr_name] = attr_value
            
            # Create the item
            items.append(config['class'](**attrs))
        
        furniture_items[furniture_type] = items
    
    # Rename keys to match variable names used elsewhere
    sofas = furniture_items['sofas']
    dining_tables = furniture_items['dining_tables']
    matresses = furniture_items['matresses']
    
    # Save all items to the database
    with Session(engine) as session:
        # Add all items to the session
        session.add_all(sofas)
        session.add_all(dining_tables)
        session.add_all(matresses)
        
        # Commit all changes to the database
        session.commit()
        
        print(f"Added {len(sofas)} sofas, {len(dining_tables)} dining tables, and {len(matresses)} mattresses to the database.")


def query_and_display_data():
    """Query and display some data from the database"""
    with Session(engine) as session:
        # Define what to query and display
        furniture_queries = [
            {
                'model': IkeaSofa,
                'title': "Sample Sofas",
                'display_fields': ['seats', 'has_sleeper']
            },
            {
                'model': IkeaDiningTable,
                'title': "Sample Dining Tables",
                'display_fields': ['seats', 'shape']
            },
            {
                'model': IkeaMatress,
                'title': "Sample Matresses",
                'display_fields': ['size', 'firmness']
            }
        ]
        
        # Query and display each furniture type
        for query_info in furniture_queries:
            items = session.exec(select(query_info['model']).limit(3)).all()
            print(f"\n--- {query_info['title']} ---")
            
            for item in items:
                # Display common info
                output = f"ID: {item.id}, {item}"
                
                # Add specific fields
                for field in query_info['display_fields']:
                    field_name = field.capitalize() if field != 'has_sleeper' else 'Sleeper'
                    output += f", {field_name}: {getattr(item, field)}"
                
                print(output)
        



def create_sample_cart():
    """Create a sample shopping cart with various furniture items"""
    with Session(engine) as session:
        # Create a new shopping cart
        cart = ShoppingCart(customer_name="John Doe", customer_email="john@example.com")
        session.add(cart)
        session.commit()
        session.refresh(cart)
        
        # Get sample furniture items of different types
        sample_items = {
            'sofas': session.exec(select(IkeaSofa).limit(2)).all(),
            'tables': session.exec(select(IkeaDiningTable).limit(1)).all(),
            'mattresses': session.exec(select(IkeaMatress).limit(3)).all()
        }
        
        # Add all items to the cart
        for item_list in sample_items.values():
            for item in item_list:
                cart.add_item(session, item, quantity=1)
        
        # Get cart summary
        summary = cart.get_cart_summary(session)
        
        # Display cart summary
        print("\n--- Sample Shopping Cart ---")
        print(f"Customer: {summary['customer']['name']} ({summary['customer']['email']})")
        print(f"Total items: {summary['total_items']}")
        print(f"Total price: ${summary['total_price']:.2f}")
        
        print("\nItems in cart:")
        for item in summary['items']:
            print(f"  {item['name']} ({item['type']}) - {item['quantity']} x ${item['price']:.2f} = ${item['subtotal']:.2f}")
        
        return cart


def main():
    """Main function to run the demo"""
    print("Creating database tables...")
    create_tables()
    
    print("Creating sample data...")
    create_sample_data()
    
    print("Querying and displaying sample data...")
    query_and_display_data()
    
    print("\nCreating a sample shopping cart...")
    create_sample_cart()
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()
