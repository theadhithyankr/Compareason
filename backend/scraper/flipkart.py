import asyncio
from playwright.async_api import async_playwright
import time
import re

async def scrape_flipkart(query: str, max_results: int = 20):
    """
    Scrape Flipkart for products based on search query
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of product dictionaries
    """
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless for production API
        page = await browser.new_page()
        
        # Set user agent to avoid bot detection
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        await page.goto(url)
        
        # Wait for page to load and try multiple selectors
        await page.wait_for_load_state('networkidle')
        
        # Try different possible selectors for product containers
        selectors_to_try = [
            "._1AtVbE",  # Your original
            "[data-id]",  # Product containers often have data-id
            "._13oc-S",   # Common product card class
            "._4rR01T",   # Title containers
            "[class*='product']",  # Any class containing 'product'
            "div[data-id]",  # More specific data-id selector
            "._2kHMtA",   # Another common product card class
            "._1fQZEK",   # Product container
            "._3pLy-c",   # Another product container
            "div[class*='_1AtVbE']",  # Variations
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

        for i, card in enumerate(product_cards[:max_results]):  # Limit to max_results
            try:
                # Extract product URL first
                link_el = await card.query_selector("a")
                url_partial = await link_el.get_attribute("href") if link_el else None
                full_url = f"https://www.flipkart.com{url_partial}" if url_partial else None

                # Extract product name from URL if available
                title = None
                if url_partial:
                    try:
                        # Flipkart URLs format: /product-name/p/product-id
                        url_parts = url_partial.split('/')
                        if len(url_parts) >= 2:
                            # Get the product name part and clean it
                            product_name_part = url_parts[1]
                            # Replace dashes with spaces and capitalize
                            title = product_name_part.replace('-', ' ').title()
                    except Exception as e:
                        pass

                # Try multiple selectors for title as backup
                if not title:
                    title_selectors = ["._4rR01T", "a[title]", "._2WkVRV", "[class*='title']", "h2", "h3"]
                    for sel in title_selectors:
                        title_el = await card.query_selector(sel)
                        if title_el:
                            title = await title_el.inner_text()
                            if title.strip():
                                break

                # Additional fallback: try to get title attribute from the link itself
                if not title and link_el:
                    try:
                        title = await link_el.get_attribute("title")
                    except Exception as e:
                        pass

                # Last resort: try to find any text that looks like a product name
                if not title:
                    try:
                        # Look for longer text elements that might be product names
                        text_elements = await card.query_selector_all("span, div, a")
                        for elem in text_elements:
                            text = await elem.inner_text()
                            if text and len(text) > 20 and len(text) < 100:  # Reasonable product name length
                                title = text.strip()
                                break
                    except Exception as e:
                        pass
                
                # Try multiple selectors for price with more comprehensive list
                price_text = None
                price_selectors = [
                    "._30jeq3",  # Common price class
                    "._1_WHN1",  # Another price class
                    "[class*='price']",  # Any class containing 'price'
                    "._3I9_wc",  # Current price
                    "._25b18c",  # Price text
                    "span[class*='price']",  # Span with price class
                    "div[class*='price']",   # Div with price class
                    "._1vC4OE",  # Another price variant
                    "._2c7tJZ",  # Price container
                    "._4b5DiR",  # Another common price class
                    "._13fcjj",  # Price container
                    "._1fQZEK",  # Discounted price
                    "._3tbKJL",  # Original price
                    "._2rQ-NK",  # Price text
                    "._3auQ3N",  # Price element
                    "._1sfVt7",  # Price container
                    "._2Tpdn3",  # Price text
                    "._3HiVg0",  # Price element
                    "._2nE8_R",  # Price container
                ]
                
                for sel in price_selectors:
                    try:
                        price_el = await card.query_selector(sel)
                        if price_el:
                            price_text = await price_el.inner_text()
                            if price_text and '₹' in price_text:
                                break
                    except Exception as e:
                        continue
                
                # If still no price found, try to get all text and find price pattern
                if not price_text:
                    try:
                        card_text = await card.inner_text()
                        
                        # Look for patterns like ₹1,23,456 or ₹12345
                        price_matches = re.findall(r'₹[\d,]+', card_text)
                        if price_matches:
                            price_text = price_matches[0]
                    except Exception as e:
                        pass
                
                # Last resort: try to find any element with rupee symbol
                if not price_text:
                    try:
                        all_elements = await card.query_selector_all("*")
                        for elem in all_elements:
                            text = await elem.inner_text()
                            if text and '₹' in text and len(text) < 20:  # Reasonable price length
                                price_text = text.strip()
                                break
                    except Exception as e:
                        pass

                # Try multiple selectors for rating
                rating = None
                rating_selectors = ["._3LWZlK", "._1lRcqv", "[class*='rating']", "._3Ay6Sb", "._3LWZlK", "._1i0wk8"]
                for sel in rating_selectors:
                    rating_el = await card.query_selector(sel)
                    if rating_el:
                        rating = await rating_el.inner_text()
                        break

                if title and price_text and full_url:
                    # Clean price text
                    try:
                        # Remove ₹ symbol and commas, then convert to int
                        cleaned_price = price_text.replace("₹", "").replace(",", "").strip()
                        # Extract only numbers
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
                        "url": full_url,
                        "rating": rating,
                        "site": "Flipkart"
                    })
                    
            except Exception as e:
                continue

        await browser.close()
        return products
