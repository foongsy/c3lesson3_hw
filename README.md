# IKEA Furniture Demo - A Python Beginner's Tutorial

Welcome to the IKEA Furniture Demo project! This tutorial will guide you through a simple but powerful Python application that demonstrates several modern Python concepts in an easy-to-understand way.

## What You'll Learn

This project shows you how to:

1. Create and use Python classes with inheritance
2. Work with a database without writing SQL code
3. Build a web API that others can use
4. Validate data to ensure it's correct
5. Create a shopping cart system

## Project Overview

This demo simulates an IKEA furniture inventory system with three types of furniture:

- **Sofas**: Comfortable seating with different fabrics and features
- **Dining Tables**: Tables with various shapes and sizes
- **Mattresses**: Different sizes and firmness levels

The project also includes a shopping cart system where customers can add furniture items.

## Getting Started

### Prerequisites

Before you begin, make sure you have:

- Python 3.7 or newer installed
- Basic understanding of Python concepts (variables, functions, etc.)

### Installation

1. Clone or download this project to your computer
2. Open a terminal/command prompt in the project folder
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Project Components

### 1. Data Models (`ikea_furniture.py`)

This file contains the definitions of our furniture items and shopping cart:

- `IkeaFurniture`: The parent class for all furniture items
- `IkeaSofa`, `IkeaDiningTable`, `IkeaMatress`: Specific furniture types
- `ShoppingCart` and `CartItem`: Classes for the shopping cart functionality

### 2. Web API (`main.py`)

This file creates a web API using FastAPI that allows you to:

- Create, read, update, and delete furniture items
- Create and manage shopping carts
- Add and remove items from shopping carts

## Running the Demo

You can run the project in two different ways:

### Option 1: Run the Database Demo

This will create sample furniture items and a shopping cart in the database:

```bash
python ikea_furniture.py
```

This will:
- Create database tables
- Add sample furniture items
- Create a sample shopping cart
- Display the items and cart information

### Option 2: Run the Web API

This will start a web server that you can interact with:

```bash
python main.py
```

Once running, you can:
1. Open your browser and go to `http://localhost:8000/docs`
2. See all available API endpoints
3. Try out the API by creating furniture items and shopping carts

## Key Concepts Explained

### SQLModel

SQLModel is a library that combines SQLAlchemy (for database operations) and Pydantic (for data validation). It lets you:

- Define your data models as Python classes
- Automatically create database tables from those classes
- Validate data before saving it to the database

### FastAPI

FastAPI is a modern web framework for building APIs. It:

- Automatically creates API documentation
- Validates incoming data
- Has great performance

### Type Hinting

Type hints help you and your code editor understand what type of data should be used. For example:

```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

This tells us that `a` and `b` should be integers, and the function returns an integer.

## Learning Exercises

Here are some things you can try to better understand the code:

1. Add a new furniture type (e.g., `IkeaBookshelf`)
2. Add a new field to an existing furniture type
3. Create a new shopping cart and add items to it
4. Modify the API to add a new endpoint

## Troubleshooting

- If you see an error about missing modules, make sure you've run `pip install -r requirements.txt`
- If the database is in a bad state, you can delete the `ikea_furniture.db` file and restart

## Next Steps

Once you're comfortable with this project, you might want to learn about:

- Adding user authentication to the API
- Creating a frontend user interface
- Deploying the application to a web server
- Adding more complex database relationships
