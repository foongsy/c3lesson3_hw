# IKEA Furniture Store API and UI

A FastAPI and Streamlit application for managing IKEA furniture inventory and shopping carts.

## Features

### Backend (FastAPI)

- CRUD operations for furniture items:
  - Sofas
  - Dining Tables
  - Mattresses
- Shopping cart functionality
- Filtering and search capabilities
- SQLite database with SQLModel ORM

### Frontend (Streamlit)

- User-friendly interface for all API operations
- Browse furniture with filters:
  - Price range
  - Materials
  - Specific features (sleeper sofas, extendable tables, etc.)
- Shopping cart management:
  - Create new carts
  - Add/remove items
  - View cart totals
- Interactive forms for adding and editing items

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI backend:

```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation is available at `http://localhost:8000/docs`

2. Start the Streamlit frontend (in a new terminal):

```bash
streamlit run app.py
```

The UI will open automatically in your default web browser

## API Endpoints

### Furniture Endpoints

- `/sofas/` - CRUD operations for sofas
- `/dining-tables/` - CRUD operations for dining tables
- `/mattresses/` - CRUD operations for mattresses

### Shopping Cart Endpoints

- `/carts/` - Create and manage shopping carts
- `/carts/{cart_id}/items` - Manage items in a cart
- `/carts/{cart_id}/total` - Get cart totals

## Project Structure

## Technologies Used

- FastAPI - Backend API framework
- Streamlit - Frontend UI framework
- SQLModel - SQL database ORM
- SQLite - Database
- Python 3.8+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)
