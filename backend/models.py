from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

class ProductResponse(BaseModel):
    title: str
    price: Union[str, int, float]
    url: str
    rating: Optional[str] = None
    site: str

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 20

class SearchResponse(BaseModel):
    products: List[ProductResponse]
    total_found: int
    query: str

class ComparisonRequest(BaseModel):
    query: str
    max_results_per_site: Optional[int] = 10
    sites: Optional[List[str]] = None

class SiteResult(BaseModel):
    status: str
    count: Optional[int] = None
    products: List[ProductResponse] = []
    error: Optional[str] = None

class PriceRange(BaseModel):
    min: float
    max: float
    avg: float

class Statistics(BaseModel):
    total_products: int
    price_range: Optional[PriceRange] = None

class BestDeals(BaseModel):
    cheapest_overall: Optional[ProductResponse] = None
    most_expensive: Optional[ProductResponse] = None
    best_per_site: Optional[Dict[str, ProductResponse]] = None
    top_5_cheapest: Optional[List[ProductResponse]] = None

class ComparisonResponse(BaseModel):
    query: str
    sites: Dict[str, SiteResult]
    all_products: List[ProductResponse]
    best_deals: BestDeals
    statistics: Optional[Statistics] = None
