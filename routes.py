from flask import Blueprint, jsonify, request
import requests
from dataclasses import asdict
from TokenModel import Token
import FoodModel, RecipeModel
import fatsecret_mapper, fatsecret_client 
from utils.parse_dataclass import parse_dataclass

api = Blueprint("api", __name__)

@api.route("/health")
def health():
    return jsonify(status="ok")
    
@api.route("/food/<food_name>")
def food(food_name):
    breakpoint()
    brand = request.args.get("brand")
    search_exp = food_name
    if brand:
        search_exp = f'{food_name} "{brand}"'

    response = fatsecret_client.search_foods(search_exp, max_results=30)
    #return jsonify(response.json())
    data = fatsecret_mapper.handle_response_data(response)
    return jsonify(data.to_dict())

@api.route("/recipe", methods=["POST"])
def recipes():
    data = parse_dataclass(RecipeModel.RecipesSearch)
    response = fatsecret_client.search_recipes(data)
    return jsonify(response)
