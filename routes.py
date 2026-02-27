from flask import Blueprint, jsonify, request
import requests
from dataclasses import asdict
from TokenModel import Token
import FoodModel
from auth import get_access_token, invalidate_token

api = Blueprint("api", __name__)

@api.route("/health")
def health():
    return jsonify(status="ok")
    
@api.route("/food/<food_name>")
def food(food_name):
    token = get_access_token()
    breakpoint()
    brand = request.args.get("brand")
    search_exp = food_name
    if brand:
        search_exp = f'{food_name} "{brand}"'

    request_data = FoodModel.FoodSearch(method="food.search", 
                                       search_expression=search_exp, 
                                       format="json"
    )
    breakpoint()
    response = requests.get(
        "https://platform.fatsecret.com/rest/foods/search/v1", 
        headers={"Authorization": f"{token.token_type} {token.access_token}"}, 
        data=asdict(requestData), 
        timeout=20 
    )

    if response.status_code == 401:
        invalidate_token()
        token = get_access_token()
        response = requests.get(
        "https://platform.fatsecret.com/rest/foods/search/v1", 
        headers={"Authorization": f"{token.token_type} {token.access_token}"}, 
        data=asdict(request_data), 
        timeout=20 
    )
        
    response.raise_for_status()
    data = response.json()
    return jsonify(data)