# Compareason - Multi-Site Price Comparison App

A full-stack price comparison application that scrapes product data from multiple e-commerce sites (Flipkart, Amazon, Reliance Digital) and provides a beautiful React frontend for comparing prices in real-time.

## 🚀 Features

- **Multi-site scraping**: Flipkart, Amazon, and Reliance Digital
- **Real-time price comparison**: Find the best deals across all sites
- **Beautiful React UI**: Clean, responsive interface with Tailwind CSS
- **Async processing**: Fast concurrent scraping using Playwright
- **RESTful API**: FastAPI backend with interactive documentation
- **Error handling**: Graceful handling of site failures and network issues

## 🏗️ Architecture

```
compareason/
├── backend/                    ← FastAPI server
│   ├── main.py                ← API endpoints and server setup
│   ├── scraper/               ← Web scraping modules
│   │   ├── flipkart.py        ← Flipkart scraper
│   │   ├── amazon.py          ← Amazon scraper
│   │   └── reliance.py        ← Reliance Digital scraper
│   ├── models.py              ← Pydantic data models
│   └── comparison_service.py  ← Multi-site comparison logic
├── frontend/                   ← React + Vite frontend
│   ├── src/
│   │   ├── App.jsx            ← Main React component
│   │   ├── main.jsx           ← React entry point
│   │   └── index.css          ← Tailwind CSS styles
│   ├── package.json           ← Frontend dependencies
│   ├── vite.config.js         ← Vite configuration
│   └── tailwind.config.js     ← Tailwind CSS configuration
├── requirements.txt           ← Python dependencies
└── README.md                  ← This file
```

## 📦 Installation

### Backend Setup

1. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

2. **Install Playwright browsers**:

```bash
playwright install
```

### Frontend Setup

1. **Navigate to frontend directory**:

```bash
cd frontend
```

2. **Install Node.js dependencies**:

```bash
npm install
```

## 🚦 Running the Application

### 1. Start the Backend Server

```bash
cd backend
python main.py
```

The API will be available at: `http://localhost:8000`

### 2. Start the Frontend Server

```bash
cd frontend
npx vite
```

The frontend will be available at: `http://localhost:5173`

## 🎯 Usage

1. **Open your browser** and navigate to `http://localhost:5173`
2. **Enter a product name** in the search box (e.g., "Samsung Galaxy M14", "iPhone 15")
3. **Click "Compare Prices"** to search across all sites
4. **View results** with prices, ratings, and direct links to products

## 🔧 API Endpoints

### GET /

- **Description**: Returns API information and available endpoints
- **Response**: API version, supported sites, and endpoint descriptions

### POST /search

- **Description**: Search products on a single site (Flipkart)
- **Request**: `{"query": "iPhone 14", "max_results": 20}`
- **Response**: List of products from Flipkart

### POST /compare

- **Description**: Compare products across multiple sites
- **Request**: `{"query": "iPhone 14", "max_results_per_site": 10, "sites": ["flipkart", "amazon", "reliance"]}`
- **Response**: Comprehensive comparison data with best deals and statistics

### GET /status

- **Description**: Check the health status of all scraping sites
- **Response**: Status of Flipkart, Amazon, and Reliance Digital scrapers

### GET /health

- **Description**: API health check
- **Response**: Server status and uptime

## 📊 API Response Format

### Compare Response

```json
{
  "query": "Samsung Galaxy M14",
  "sites": {
    "flipkart": {
      "products": [
        {
          "title": "Samsung Galaxy M14 5G (Berry Blue, 128 GB)",
          "price": 14990,
          "url": "https://www.flipkart.com/samsung-galaxy-m14-5g-berry-blue-128-gb/p/...",
          "rating": "4.3",
          "site": "Flipkart"
        }
      ],
      "total_found": 1,
      "error": null
    },
    "amazon": {
      /* similar structure */
    },
    "reliance": {
      /* similar structure */
    }
  },
  "best_deals": {
    "cheapest_overall": {
      "title": "Samsung Galaxy M14 5G (Berry Blue, 128 GB)",
      "price": 14990,
      "site": "Flipkart",
      "url": "https://www.flipkart.com/...",
      "rating": "4.3"
    },
    "most_expensive": {
      /* similar structure */
    },
    "best_per_site": {
      "flipkart": {
        /* best deal from Flipkart */
      },
      "amazon": {
        /* best deal from Amazon */
      },
      "reliance": {
        /* best deal from Reliance */
      }
    }
  },
  "statistics": {
    "total_products": 25,
    "price_range": "₹14,990 - ₹18,999"
  }
}
```

## 🖥️ Frontend Features

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Search**: Live product comparison across multiple sites
- **Site Selection**: Choose which sites to search
- **Best Deal Highlighting**: Automatically identifies cheapest options
- **Error Handling**: Graceful handling of API failures
- **Loading States**: Visual feedback during searches

## 🛠️ Technology Stack

### Backend

- **FastAPI**: Modern, fast web framework for APIs
- **Playwright**: Reliable web scraping and automation
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment
- **Asyncio**: Concurrent scraping for better performance

### Frontend

- **React 18**: Modern UI library with hooks
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library

## 🧪 Testing

### Backend API Testing

```bash
# Test the compare endpoint
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{"query": "iPhone 15", "max_results_per_site": 5}'

# Check site status
curl "http://localhost:8000/status"
```

### Frontend Testing

1. Open `http://localhost:5173` in your browser
2. Search for popular products like:
   - "Samsung Galaxy M14"
   - "iPhone 15"
   - "Sony headphones"
   - "Nike shoes"
   - "Dell laptop"

## 📚 Interactive Documentation

Once the backend server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Production Deployment

### Backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
npm run preview
```

## 🔮 Future Enhancements

- **Database Integration**: PostgreSQL/Supabase for price history
- **Power BI Dashboard**: Analytics and price trend visualization
- **Price Alerts**: Email notifications for price drops
- **User Accounts**: Save favorites and search history
- **Mobile App**: React Native version
- **More Sites**: Integration with additional e-commerce platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, email your-email@example.com or create an issue in the GitHub repository.

---

**Built with ❤️ using FastAPI, React, and Playwright**
