import asyncio
from playwright.async_api import async_playwright
import time
import re

async def scrape_amazon(query: str, max_results: int = 20):
    """
    Scrape Amazon for products based on search query
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of product dictionaries
    """
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
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
            
            # Try different selectors for Amazon product containers
            selectors_to_try = [
                "[data-component-type='s-search-result']",
                ".s-result-item",
                "[data-cy='title-recipe-label']",
                ".a-section.a-spacing-medium",
                "[data-asin]"
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
                        "h2 a span",
                        "h2 span",
                        ".a-size-medium",
                        ".a-size-base-plus",
                        "[data-cy='title-recipe-label']",
                        ".s-size-mini"
                    ]
                    
                    for sel in title_selectors:
                        title_el = await card.query_selector(sel)
                        if title_el:
                            title = await title_el.inner_text()
                            if title and title.strip():
                                title = title.strip()
                                break
                    
                    # Extract price
                    price_text = None
                    price_selectors = [
                        ".a-price-whole",
                        ".a-price .a-offscreen",
                        ".a-price-range",
                        ".a-price",
                        ".a-offscreen"
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
                        ".a-icon-alt",
                        ".a-star-medium",
                        "[aria-label*='star']"
                    ]
                    
                    for sel in rating_selectors:
                        rating_el = await card.query_selector(sel)
                        if rating_el:
                            rating_text = await rating_el.get_attribute("aria-label")
                            if not rating_text:
                                rating_text = await rating_el.inner_text()
                            if rating_text and "star" in rating_text.lower():
                                # Extract rating number
                                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                                if rating_match:
                                    rating = rating_match.group(1)
                                    break
                    
                    # Extract product URL
                    url_el = await card.query_selector("h2 a")
                    if not url_el:
                        url_el = await card.query_selector("a")
                    
                    product_url = None
                    if url_el:
                        href = await url_el.get_attribute("href")
                        if href:
                            if href.startswith('/'):
                                product_url = f"https://www.amazon.in{href}"
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
                            "site": "Amazon"
                        })
                        
                except Exception as e:
                    continue
            
            await browser.close()
            return products
            
        except Exception as e:
            await browser.close()
            return []
