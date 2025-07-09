import asyncio
from playwright.async_api import async_playwright
import time
import re

async def scrape_reliance(query: str, max_results: int = 20):
    """
    Scrape Reliance Digital for products based on search query
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of product dictionaries
    """
    url = f"https://www.reliancedigital.in/search?q={query.replace(' ', '%20')}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set user agent to avoid bot detection
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state('networkidle')
            
            # Try different selectors for Reliance Digital product containers
            selectors_to_try = [
                ".sp__product",
                ".product-item",
                ".product-card",
                "[data-testid='product-card']",
                ".search-product-item"
            ]
            
            products = []
            product_cards = []
            
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    product_cards = await page.query_selector_all(selector)
                    if product_cards:
                        break
                except:
                    continue
            
            if not product_cards:
                await browser.close()
                return []

            for i, card in enumerate(product_cards[:max_results]):
                try:
                    # Extract product title
                    title = None
                    title_selectors = [
                        ".sp__name",
                        ".product-title",
                        ".product-name",
                        "h3",
                        "h2",
                        ".title",
                        "a[title]"
                    ]
                    
                    for sel in title_selectors:
                        title_el = await card.query_selector(sel)
                        if title_el:
                            title = await title_el.inner_text()
                            if title and title.strip():
                                title = title.strip()
                                break
                    
                    # Try to get title from link attribute
                    if not title:
                        link_el = await card.query_selector("a")
                        if link_el:
                            title = await link_el.get_attribute("title")
                    
                    # Extract price
                    price_text = None
                    price_selectors = [
                        ".sp__price",
                        ".price",
                        ".current-price",
                        ".offer-price",
                        ".sp__offer-price",
                        "[data-testid='price']"
                    ]
                    
                    for sel in price_selectors:
                        price_el = await card.query_selector(sel)
                        if price_el:
                            price_text = await price_el.inner_text()
                            if price_text and '₹' in price_text:
                                break
                    
                    # If no price found, try regex on card text
                    if not price_text:
                        try:
                            card_text = await card.inner_text()
                            price_matches = re.findall(r'₹[\d,]+', card_text)
                            if price_matches:
                                price_text = price_matches[0]
                        except:
                            pass
                    
                    # Extract rating
                    rating = None
                    rating_selectors = [
                        ".sp__rating",
                        ".rating",
                        ".star-rating",
                        "[data-testid='rating']"
                    ]
                    
                    for sel in rating_selectors:
                        rating_el = await card.query_selector(sel)
                        if rating_el:
                            rating_text = await rating_el.inner_text()
                            if rating_text:
                                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                                if rating_match:
                                    rating = rating_match.group(1)
                                    break
                    
                    # Extract product URL
                    url_el = await card.query_selector("a")
                    product_url = None
                    if url_el:
                        href = await url_el.get_attribute("href")
                        if href:
                            if href.startswith('/'):
                                product_url = f"https://www.reliancedigital.in{href}"
                            else:
                                product_url = href
                    
                    if title and price_text and product_url:
                        # Clean price
                        try:
                            cleaned_price = price_text.replace("₹", "").replace(",", "").strip()
                            price_numbers = re.findall(r'\d+', cleaned_price)
                            if price_numbers:
                                price = int(''.join(price_numbers))
                            else:
                                price = price_text
                        except:
                            price = price_text
                        
                        products.append({
                            "title": title,
                            "price": price,
                            "url": product_url,
                            "rating": rating,
                            "site": "Reliance Digital"
                        })
                        
                except Exception as e:
                    continue
            
            await browser.close()
            return products
            
        except Exception as e:
            await browser.close()
            return []
