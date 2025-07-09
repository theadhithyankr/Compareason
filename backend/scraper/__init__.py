# Scraper package for various e-commerce sites
from .flipkart import scrape_flipkart
from .amazon import scrape_amazon
from .reliance import scrape_reliance

__all__ = ["scrape_flipkart", "scrape_amazon", "scrape_reliance"]
