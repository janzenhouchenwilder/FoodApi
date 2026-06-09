from functools import wraps

from flask import Blueprint, jsonify, request
import requests
from dataclasses import asdict
from TokenModel import Token
import FoodModel, RecipeModel
import fatsecret_mapper, fatsecret_client 
from utils.parse_dataclass import parse_dataclass
from auth import validate_auth

api = Blueprint("api", __name__)

@api.route("/health")
def health():
    return jsonify(status="ok")

def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not validate_auth(request.headers.get("X-API-Key")):
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper
    
@api.route("/food/<food_name>")
@require_api_key
def food(food_name):
    brand = request.args.get("brand")
    search_exp = food_name
    if brand:
        search_exp = f'{food_name} "{brand}"'

    response = fatsecret_client.search_foods(search_exp, max_results=30)
    #return jsonify(response.json())
    data = fatsecret_mapper.handle_response_data(response)
    return jsonify(data.to_dict())

@api.route("/food/id/<id>")
@require_api_key
def food_by_id(id):
    brand = request.args.get("brand")
    search_exp = id
    if brand:
        search_exp = f'{id} "{brand}"'

    response = fatsecret_client.search_food_by_id(search_exp)
#    data = fatsecret_mapper.handle_response_data_by_id(response)
    return jsonify(response)

@api.route("/recipe", methods=["POST"])
@require_api_key
def recipes():
    data = parse_dataclass(RecipeModel.RecipesSearch)
    response = fatsecret_client.search_recipes(data)
    return jsonify(response)
