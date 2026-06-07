from dataclasses import dataclass, asdict
from typing import Optional, List, Union


# @dataclass
# class Food:
#     food_description: str
#     food_id: str
#     food_name: str
#     food_type: str
#     food_url: str
#     brand_name: Optional[str] = None

#     def to_dict(self) -> dict:
#         return asdict(self)
        

@dataclass
class FoodDescription:
    serving_size: str
    calories: str
    fat: str
    carbs: str
    protein: str

    def to_dict(self) -> dict:
        return asdict(self)
    
#Object that gets returned 
@dataclass
class Food:
    food_id: str
    food_name: str
    food_type: str
    food_url: str
    food_description: FoodDescription
    brand_name: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}
    
@dataclass
class Foods:
    food: List[Food]
    max_results: str
    page_number: str
    total_results: str

    def to_dict(self) -> dict:
        return asdict(self)
    
@dataclass
class FoodRoot:
    foods: Foods

    def to_dict(self) -> dict:
        return asdict(self)

#Request object 
@dataclass
class FoodSearch:
    method: str
    search_expression: str
    format: str
    max_results: int

@dataclass
class FoodSearchById:
    method: str
    food_id: str
    format: str

@dataclass
class Serving:
    calcium: str
    calories: str
    carbohydrate: str
    cholesterol: str
    fat: str
    fiber: str
    iron: str
    measurement_description: str
    metric_serving_amount: str
    metric_serving_unit: str
    monounsaturated_fat: str
    number_of_units: str
    polyunsaturated_fat: str
    potassium: str
    protein: str
    saturated_fat: str
    serving_description: str
    serving_id: str
    serving_url: str
    sodium: str
    sugar: str
    vitamin_a: str
    vitamin_c: str


@dataclass
class Servings:
    serving: List[Serving]

@dataclass
class FoodIdDetail:
    food_id: str
    food_name: str
    food_type: str
    food_url: str
    servings: Servings

@dataclass
class FoodIdSearchResponse:
    food: Food
    