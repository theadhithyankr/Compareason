import asyncio
from typing import List, Dict, Any
from scraper.flipkart import scrape_flipkart
from scraper.amazon import scrape_amazon
from scraper.reliance import scrape_reliance

class ComparisonService:
    """Service for comparing products across multiple e-commerce sites"""
    
    def __init__(self):
        self.scrapers = {
            'flipkart': scrape_flipkart,
            'amazon': scrape_amazon,
            'reliance': scrape_reliance
        }
    
    async def compare_products(self, query: str, max_results_per_site: int = 10, sites: List[str] = None) -> Dict[str, Any]:
        """
        Compare products across multiple sites
        
        Args:
            query: Search query string
            max_results_per_site: Maximum results per site
            sites: List of sites to search (default: all)
        
        Returns:
            Dictionary with comparison results
        """
        if sites is None:
            sites = list(self.scrapers.keys())
        
        # Create tasks for concurrent scraping
        tasks = []
        for site in sites:
            if site in self.scrapers:
                task = asyncio.create_task(
                    self.scrapers[site](query, max_results_per_site),
                    name=site
                )
                tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        comparison_data = {
            'query': query,
            'sites': {},
            'all_products': [],
            'best_deals': {
                'cheapest_overall': None,
                'most_expensive': None,
                'best_per_site': None,
                'top_5_cheapest': None
            },
            'statistics': {
                'total_products': 0,
                'price_range': None
            }
        }
        
        total_products = 0
        all_prices = []
        
        for i, result in enumerate(results):
            site_name = sites[i] if i < len(sites) else f"site_{i}"
            
            if isinstance(result, Exception):
                comparison_data['sites'][site_name] = {
                    'status': 'error',
                    'error': str(result),
                    'products': []
                }
                continue
            
            products = result if isinstance(result, list) else []
            comparison_data['sites'][site_name] = {
                'status': 'success',
                'count': len(products),
                'products': products
            }
            
            # Add site name to each product and collect all products
            for product in products:
                comparison_data['all_products'].append(product)
                if isinstance(product.get('price'), (int, float)):
                    all_prices.append(product['price'])
            
            total_products += len(products)
        
        # Calculate statistics
        comparison_data['statistics']['total_products'] = total_products
        
        if all_prices:
            comparison_data['statistics']['price_range'] = {
                'min': min(all_prices),
                'max': max(all_prices),
                'avg': sum(all_prices) / len(all_prices)
            }
            
            # Find best deals
            comparison_data['best_deals'] = self._find_best_deals(comparison_data['all_products'])
        
        return comparison_data
    
    def _find_best_deals(self, products: List[Dict]) -> Dict[str, Any]:
        """Find the best deals from all products"""
        if not products:
            return {
                'cheapest_overall': None,
                'most_expensive': None,
                'best_per_site': None,
                'top_5_cheapest': None
            }
        
        # Filter products with valid prices
        valid_products = [p for p in products if isinstance(p.get('price'), (int, float))]
        
        if not valid_products:
            return {
                'cheapest_overall': None,
                'most_expensive': None,
                'best_per_site': None,
                'top_5_cheapest': None
            }
        
        # Sort by price (lowest first)
        sorted_by_price = sorted(valid_products, key=lambda x: x['price'])
        
        # Group by site for best deal per site
        site_best = {}
        for product in valid_products:
            site = product.get('site', 'unknown')
            if site not in site_best or product['price'] < site_best[site]['price']:
                site_best[site] = product
        
        return {
            'cheapest_overall': sorted_by_price[0] if sorted_by_price else None,
            'most_expensive': sorted_by_price[-1] if sorted_by_price else None,
            'best_per_site': site_best if site_best else None,
            'top_5_cheapest': sorted_by_price[:5] if sorted_by_price else None
        }
    
    async def get_site_status(self) -> Dict[str, str]:
        """Check the status of all scraping sites"""
        status = {}
        
        for site_name in self.scrapers:
            try:
                # Try a quick test search
                result = await self.scrapers[site_name]("test", 1)
                status[site_name] = "online" if isinstance(result, list) else "offline"
            except Exception as e:
                status[site_name] = f"error: {str(e)[:50]}..."
        
        return status

# Create a global instance
comparison_service = ComparisonService()
