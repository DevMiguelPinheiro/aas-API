# FastAPI MongoDB API

This is a RESTful API built with FastAPI and MongoDB, providing CRUD operations for items.

## Prerequisites

- Python 3.7+
- MongoDB running locally or a MongoDB Atlas account

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fastapi_db
```

## Running the Application

Start the server with:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Available Endpoints

- `POST /items/` - Create a new item
- `GET /items/` - List all items
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

## Example Item Structure

```json
{
    "name": "Sample Item",
    "description": "This is a sample item",
    "price": 29.99,
    "quantity": 10
}
``` 