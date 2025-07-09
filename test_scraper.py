#!/usr/bin/env python3
"""
Test script for the Flipkart scraper API
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from scraper.flipkart import scrape_flipkart

async def test_scraper():
    """Test the scraper function directly"""
    print("Testing Flipkart scraper...")
    
    query = "iPhone 14"
    max_results = 5
    
    print(f"Searching for: {query}")
    print(f"Max results: {max_results}")
    print("-" * 50)
    
    try:
        products = await scrape_flipkart(query, max_results)
        print(f"Found {len(products)} products:")
        print("=" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['title']}")
            print(f"   Price: {product['price']}")
            print(f"   Rating: {product['rating']}")
            print(f"   URL: {product['url']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
