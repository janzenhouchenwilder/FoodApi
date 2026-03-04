import requests
from dataclasses import asdict
import FoodModel
from auth import get_access_token, invalidate_token

FATSECRET_SEARCH_URL = "https://platform.fatsecret.com/rest/foods/search/v1"

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