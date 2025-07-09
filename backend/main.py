from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import (
    ProductResponse, SearchRequest, SearchResponse, 
    ComparisonRequest, ComparisonResponse
)
from scraper.flipkart import scrape_flipkart
from comparison_service import comparison_service

# FastAPI app setup
app = FastAPI(
    title="Compareason - Multi-Site Product Comparison API",
    version="2.0.0",
    description="A comprehensive FastAPI application for comparing products across multiple e-commerce sites"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Root endpoint with basic API information
    """
    return {
        "message": "Compareason - Multi-Site Product Comparison API",
        "version": "2.0.0",
        "docs": "/docs",
        "supported_sites": ["flipkart", "amazon", "reliance"],
        "endpoints": {
            "POST /search": "Search products on single site",
            "GET /search/{query}": "Search products on single site with query parameter",
            "POST /compare": "Compare products across multiple sites",
            "GET /compare/{query}": "Compare products across multiple sites with query parameter",
            "GET /status": "Check status of all supported sites"
        }
    }

@app.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Search for products on Flipkart using POST request
    
    Args:
        request: SearchRequest containing query and max_results
        
    Returns:
        SearchResponse with products list and metadata
    """
    try:
        products = await scrape_flipkart(request.query, request.max_results)
        return SearchResponse(
            products=products,
            total_found=len(products),
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping products: {str(e)}")

@app.get("/search/{query}")
async def search_products_get(query: str, max_results: int = 20):
    """
    Search for products on Flipkart using GET request
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 20)
        
    Returns:
        SearchResponse with products list and metadata
    """
    try:
        products = await scrape_flipkart(query, max_results)
        return SearchResponse(
            products=products,
            total_found=len(products),
            query=query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping products: {str(e)}")

@app.post("/compare", response_model=ComparisonResponse)
async def compare_products(request: ComparisonRequest):
    """
    Compare products across multiple e-commerce sites
    
    Args:
        request: ComparisonRequest containing query, max_results_per_site, and sites
        
    Returns:
        ComparisonResponse with products from all sites and comparison data
    """
    try:
        comparison_data = await comparison_service.compare_products(
            request.query, 
            request.max_results_per_site, 
            request.sites
        )
        return ComparisonResponse(**comparison_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing products: {str(e)}")

@app.get("/compare/{query}")
async def compare_products_get(query: str, max_results_per_site: int = 10, sites: str = None):
    """
    Compare products across multiple e-commerce sites using GET request
    
    Args:
        query: Search query string
        max_results_per_site: Maximum results per site (default: 10)
        sites: Comma-separated list of sites to search (default: all)
        
    Returns:
        ComparisonResponse with products from all sites and comparison data
    """
    try:
        sites_list = sites.split(',') if sites else None
        comparison_data = await comparison_service.compare_products(
            query, 
            max_results_per_site, 
            sites_list
        )
        return ComparisonResponse(**comparison_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing products: {str(e)}")

@app.get("/status")
async def get_site_status():
    """
    Check the status of all supported scraping sites
    
    Returns:
        Dictionary with status of each site
    """
    try:
        status = await comparison_service.get_site_status()
        return {
            "status": "success",
            "sites": status,
            "timestamp": "2025-07-09T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking site status: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
