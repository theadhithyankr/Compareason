"""
Simple test script to verify the scraper works
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_api_locally():
    """Test the API components locally"""
    print("Testing the scraper locally...")
    
    try:
        from scraper.flipkart import scrape_flipkart
        
        # Test with a simple query
        query = "mobile phone"
        max_results = 2
        
        print(f"Searching for: {query}")
        print(f"Max results: {max_results}")
        print("-" * 50)
        
        products = await scrape_flipkart(query, max_results)
        
        if products:
            print(f"✅ Success! Found {len(products)} products:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product['title']}")
                print(f"   Price: ₹{product['price']}")
                print(f"   Rating: {product.get('rating', 'N/A')}")
                print(f"   URL: {product['url'][:50]}...")
                print("-" * 30)
        else:
            print("❌ No products found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_locally())
