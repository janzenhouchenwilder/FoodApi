import requests
from dataclasses import asdict
from typing import List
import FoodModel, RecipeModel
from auth import get_access_token, invalidate_token

FATSECRET_SEARCH_URL = "https://platform.fatsecret.com/rest/foods/search/v1"
FATSECRET_RECIPE_URL = "https://platform.fatsecret.com/rest/recipes/search/v3"

def search_foods(search_exp: str, max_results: int = 10) -> dict:
    token = get_access_token()

    req = FoodModel.FoodSearch(
        method="foods.search",
        search_expression=search_exp,
        format="json",
        max_results=max_results
    )

    resp = requests.get(
        FATSECRET_SEARCH_URL,
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
        params=asdict(req),
        timeout=20
    )

    if resp.status_code == 401:
        invalidate_token()
        token = get_access_token()
        resp = requests.get(
            FATSECRET_SEARCH_URL,
            headers={"Authorization": f"{token.token_type} {token.access_token}"},
            params=asdict(req),
            timeout=20
        )

    resp.raise_for_status()
    return resp.json()

def search_recipes(recipe_search: RecipeModel.RecipesSearch) -> dict:
    token = get_access_token()

    req = recipe_search
    # full_request: dict = {}
    # #api has properties with . instead of _ so I am handling that here
    # not_valid_dict: dict = { "carb_percentage_to": "carb_percentage.to", 
    #                         "fat_percentage_to": "fat_percentage.to", 
    #                         "protein_percentage_to": "protein_percentage.to", 
    #                         "prep_time_to": "prep_time.to" 
    # }
    # #if key is not fatsecret key with . then add it from the values of not_valid_dict 
    # #and take the key value from fatsecret_dict 
    # for key, val in fatsecret_dict.items():
    #     if key not in not_valid_dict:
    #         full_request[key] = val
    #     else:
    #         full_request[val] = fatsecret_dict[key]
    
    req.max_results = req.max_results if req.max_results else 30
    req.method = "recipes.search.v3"
    req.format = "json"

    full_request = req.to_dict()

    response = requests.get(
        FATSECRET_RECIPE_URL, 
        headers={"Authorization": f"{token.token_type} {token.access_token}"}, 
        params=full_request, 
        timeout=20
    )

    if response.status_code == 401:
        invalidate_token()
        response = requests.get(
            FATSECRET_RECIPE_URL, 
            headers={"Authorization": f"{token.token_type} {token.access_token}"}, 
            params=full_request, 
            timeout=20
        )

    response.raise_for_status()
    return response.json()