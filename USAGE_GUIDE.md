# 🚀 How to Use Your Flipkart Scraper API

## Quick Start Guide

### 1. **Start the Server**

```bash
# Option 1: Using the batch file (Windows)
double-click run_api.bat

# Option 2: Using PowerShell
.\run_api.ps1

# Option 3: Manual command
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. **Access the API**

- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🎯 How to Use the API

### **Method 1: Using the Interactive Documentation (Easiest)**

1. Go to: http://localhost:8000/docs
2. Click on any endpoint (like `POST /search`)
3. Click "Try it out"
4. Enter your search query
5. Click "Execute"

### **Method 2: Using cURL (Command Line)**

```bash
# Search for iPhone (GET request)
curl "http://localhost:8000/search/iPhone?max_results=5"

# Search using POST request
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "Samsung mobile", "max_results": 10}'
```

### **Method 3: Using Python**

```python
import requests

# GET request
response = requests.get("http://localhost:8000/search/iPhone?max_results=5")
data = response.json()

# POST request
response = requests.post("http://localhost:8000/search",
                        json={"query": "Samsung mobile", "max_results": 10})
data = response.json()

# Print results
for product in data['products']:
    print(f"Title: {product['title']}")
    print(f"Price: ₹{product['price']}")
    print(f"URL: {product['url']}")
    print("-" * 40)
```

### **Method 4: Using JavaScript (Frontend)**

```javascript
// GET request
fetch("http://localhost:8000/search/iPhone?max_results=5")
  .then((response) => response.json())
  .then((data) => console.log(data));

// POST request
fetch("http://localhost:8000/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "Samsung mobile",
    max_results: 10,
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

## 📋 Available Endpoints

| Method | Endpoint          | Description                       |
| ------ | ----------------- | --------------------------------- |
| GET    | `/`               | API information                   |
| GET    | `/search/{query}` | Search products by URL parameter  |
| POST   | `/search`         | Search products with request body |
| GET    | `/health`         | Health check                      |
| GET    | `/docs`           | Interactive API documentation     |

## 🔧 Response Format

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

## 🛠️ Testing Your API

Run the test script:

```bash
python test_api.py
```

## 🚨 Common Issues

1. **Server not starting**: Make sure you're in the correct directory
2. **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`
3. **Playwright issues**: Run `playwright install` if you get browser errors
4. **Port already in use**: Change the port in `main.py` or kill the existing process

## 🎉 What You Can Do Next

1. **Build a Frontend**: Create a web interface using React, Vue, or plain HTML/JS
2. **Add More Sites**: Extend the scraper to support Amazon, eBay, etc.
3. **Database Integration**: Store search results in a database
4. **Caching**: Add Redis caching for faster responses
5. **Deployment**: Deploy to Heroku, AWS, or other cloud platforms

## 📱 Example Use Cases

- **Price Comparison Website**: Compare prices across multiple sites
- **Product Monitoring**: Track price changes over time
- **Market Research**: Analyze product availability and pricing
- **Shopping Assistant**: Help users find the best deals
