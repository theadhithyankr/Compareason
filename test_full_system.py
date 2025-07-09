#!/usr/bin/env python3
"""
Comprehensive test script for the Compareason multi-site scraper
"""

import asyncio
import sys
import os
import time
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from comparison_service import comparison_service

async def test_individual_scrapers():
    """Test each scraper individually"""
    print("🧪 Testing Individual Scrapers")
    print("=" * 50)
    
    test_query = "Samsung mobile"
    max_results = 3
    
    for site_name, scraper_func in comparison_service.scrapers.items():
        print(f"\n📱 Testing {site_name.title()}...")
        try:
            start_time = time.time()
            products = await scraper_func(test_query, max_results)
            end_time = time.time()
            
            print(f"✅ Success! Found {len(products)} products in {end_time - start_time:.2f}s")
            
            for i, product in enumerate(products[:2], 1):  # Show first 2 products
                print(f"  {i}. {product['title'][:50]}...")
                print(f"     Price: ₹{product['price']}")
                print(f"     Rating: {product.get('rating', 'N/A')}")
                print(f"     Site: {product['site']}")
                print()
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

async def test_comparison_service():
    """Test the comparison service"""
    print("\n🔍 Testing Comparison Service")
    print("=" * 50)
    
    test_queries = [
        "iPhone 14",
        "Samsung Galaxy M14",
        "laptop"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Testing query: '{query}'")
        try:
            start_time = time.time()
            result = await comparison_service.compare_products(query, max_results_per_site=2)
            end_time = time.time()
            
            print(f"✅ Comparison completed in {end_time - start_time:.2f}s")
            print(f"   Total products found: {len(result['all_products'])}")
            
            # Show site-wise results
            for site_name, site_data in result['sites'].items():
                status = site_data['status']
                count = site_data.get('count', 0)
                print(f"   {site_name}: {status} ({count} products)")
            
            # Show best deal if available
            if result['best_deals'].get('cheapest_overall'):
                best = result['best_deals']['cheapest_overall']
                print(f"   💰 Best deal: ₹{best['price']} on {best['site']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

async def test_site_status():
    """Test site status check"""
    print("\n🌐 Testing Site Status")
    print("=" * 50)
    
    try:
        status = await comparison_service.get_site_status()
        print("Site Status:")
        for site, site_status in status.items():
            status_emoji = "🟢" if site_status == "online" else "🔴"
            print(f"  {status_emoji} {site}: {site_status}")
    except Exception as e:
        print(f"❌ Error checking site status: {e}")

async def performance_test():
    """Test performance with multiple concurrent requests"""
    print("\n⚡ Performance Test")
    print("=" * 50)
    
    queries = ["iPhone", "Samsung", "laptop", "headphones", "mobile"]
    
    print(f"Testing {len(queries)} concurrent comparisons...")
    
    start_time = time.time()
    
    # Create tasks for concurrent execution
    tasks = []
    for query in queries:
        task = asyncio.create_task(
            comparison_service.compare_products(query, max_results_per_site=2)
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.time()
    
    print(f"✅ All {len(queries)} comparisons completed in {end_time - start_time:.2f}s")
    
    # Analyze results
    successful = sum(1 for r in results if not isinstance(r, Exception))
    failed = len(results) - successful
    
    print(f"   Successful: {successful}/{len(queries)}")
    print(f"   Failed: {failed}/{len(queries)}")
    
    if successful > 0:
        avg_time = (end_time - start_time) / successful
        print(f"   Average time per comparison: {avg_time:.2f}s")

async def main():
    """Run all tests"""
    print("🚀 Compareason Multi-Site Scraper Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    await test_individual_scrapers()
    await test_comparison_service()
    await test_site_status()
    await performance_test()
    
    print("\n🎉 Test Suite Completed!")
    print("=" * 60)
    print("Next steps:")
    print("1. Start the backend server: cd backend && python main.py")
    print("2. Install frontend dependencies: cd frontend && npm install")
    print("3. Start the frontend: cd frontend && npm run dev")
    print("4. Visit: http://localhost:3000")

if __name__ == "__main__":
    asyncio.run(main())
