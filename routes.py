from flask import Blueprint, jsonify
import config
import requests
from dataclasses import asdict
from TokenModel import Token
import FoodModel

api = Blueprint("api", __name__)

@api.route("/health")
def health():
    return jsonify(status="ok")
    
@api.route("/food/<foodName>")
def food(foodName):
    token = getCredentials()
    requestData = FoodModel.FoodSearch(method="food.search", 
                                       search_expression=foodName, 
                                       format="json"
    )
    breakpoint()
    response = requests.get(
        "https://platform.fatsecret.com/rest/foods/search/v1", 
        headers={"Authorization": f"{token.token_type} {token.access_token}"}, 
        data=asdict(requestData), 
        timeout=20 
    )
    response.raise_for_status()
    data = response.json()
    return jsonify(data)
    
def getCredentials() -> Token:
    credentials = config.getCredentials()
    response = requests.post(
        "https://oauth.fatsecret.com/connect/token",
        auth=(credentials["ClientId"], credentials["ClientSecret"]),
        data={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=20
    )
    response.raise_for_status()
    data = response.json()
    return Token(access_token = data["access_token"],
                token_type = data["token_type"],
                expires_in = data["expires_in"]
    )
    
