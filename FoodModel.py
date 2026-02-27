from dataclasses import dataclass, asdict
from typing import Optional, List, Union


@dataclass
class Food:
    brand_name: str
    food_description: str
    food_id: str
    food_name: str
    food_type: str
    food_url: str
    max_results: str
    page_number: str
    total_results: str

    def to_dict(self) -> dict:
        return asdict(self)
        
@dataclass
class Foods:
    food: Optional[Food] = None

@dataclass
class FoodSearch:
    method: str
    search_expression: str
    format: str
    