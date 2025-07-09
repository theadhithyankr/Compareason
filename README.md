# Flipkart Product Scraper API

A FastAPI-based web scraper for Flipkart products.

## Project Structure

```
compareason/
├── backend/
│   ├── main.py             ← FastAPI app
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── flipkart.py     ← Flipkart scraper logic
│   └── models.py           ← Pydantic models
├── requirements.txt        ← Dependencies
└── README.md              ← This file
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:

```bash
playwright install
```

## Running the API

### Development

```bash
cd backend
python main.py
```

### Production

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### GET /

- Returns API information and available endpoints

### POST /search

- Request body: `{"query": "iPhone 14", "max_results": 20}`
- Returns: List of products matching the search query

### GET /search/{query}

- Query parameter: `query` (required)
- Query parameter: `max_results` (optional, default: 20)
- Returns: List of products matching the search query

### GET /health

- Returns: API health status

## Example Usage

### Using cURL

```bash
# GET request
curl "http://localhost:8000/search/iPhone%2014?max_results=10"

# POST request
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "iPhone 14", "max_results": 10}'
```

### Using Python requests

```python
import requests

# GET request
response = requests.get("http://localhost:8000/search/iPhone 14?max_results=10")
data = response.json()

# POST request
response = requests.post("http://localhost:8000/search",
                        json={"query": "iPhone 14", "max_results": 10})
data = response.json()
```

## Response Format

```json
{
  "products": [
    {
      "title": "Apple iPhone 14 (128GB) - Blue",
      "price": 79900,
      "url": "https://www.flipkart.com/apple-iphone-14-blue-128-gb/p/...",
      "rating": "4.6",
      "site": "Flipkart"
    }
  ],
  "total_found": 1,
  "query": "iPhone 14"
}
```

## Interactive Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
