from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class RecipesSearch:
    method: str
    recipe_types: Optional[str] = None
    recipe_types_matchall: Optional[bool] = None
    search_expression: Optional[str] = None
    must_have_images: Optional[bool] = None

    calories_from: Optional[int] = None
    calories_to: Optional[int] = None
    carb_percentage_from: Optional[int] = None
    carb_percentage_to: Optional[int] = None
    protein_percentage_from: Optional[int] = None
    protein_percentage_to: Optional[int] = None
    fat_percentage_from: Optional[int] = None
    fat_percentage_to: Optional[int] = None
    prep_time_from: Optional[int] = None
    prep_time_to: Optional[int] = None

    page_number: Optional[int] = None
    max_results: Optional[int] = None
    sort_by: Optional[str] = None
    format: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)

        mapping = {
        "carb_percentage_to": "carb_percentage.to",
        "carb_percentage_from": "carb_percentage.from",
        "fat_percentage_to": "fat_percentage.to",
        "fat_percentage_from": "fat_percentage.from",
        "protein_percentage_to": "protein_percentage.to",
        "protein_percentage_from": "protein_percentage.from",
        "prep_time_to": "prep_time.to",
        "prep_time_from": "prep_time.from",
        "calories_to": "calories.to",
        "calories_from": "calories.from",
        }

        transformed = {}

        for k, v in data.items():
            if v is None:
                continue
            transformed[mapping.get(k, k)] = v

        return transformed
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class RecipeNutrition:
    calories: str
    carbohydrate: str
    fat: str
    protein: str


@dataclass
class RecipeIngredients:
    ingredient: List[str]


@dataclass
class RecipeTypes:
    recipe_type: List[str]


@dataclass
class Recipe:
    recipe_description: str
    recipe_id: str
    recipe_image: str
    recipe_ingredients: RecipeIngredients
    recipe_name: str
    recipe_nutrition: RecipeNutrition
    recipe_types: RecipeTypes


@dataclass
class Recipes:
    max_results: str
    page_number: str
    total_results: str
    recipe: List[Recipe]

@dataclass
class RecipesResponse:
    recipes: Recipes

    def to_dict(self) -> dict:
        return asdict(self)
