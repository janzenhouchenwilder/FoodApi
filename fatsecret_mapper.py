import FoodModel

def handle_response_data(json: {}) -> FoodModel.FoodRoot:
    foods_data = json["foods"]
    max_results = foods_data["max_results"]
    total_results = foods_data["total_results"]
    page_number = foods_data["page_number"]
    items = foods_data["food"]

    if not isinstance(items, list):
        items = [items]

    foods = []

    for item in items:
        desc = handle_food_description(item["food_description"])
        food = FoodModel.Food(
                food_id=item["food_id"],
                food_name=item["food_name"],
                food_type=item["food_type"],
                food_url=item["food_url"],
                food_description=desc
            ).to_dict()
        if "brand_name" in item:
            food["brand_name"] = item["brand_name"]
        foods.append(food)

    return FoodModel.FoodRoot(
        foods=FoodModel.Foods(food=foods, 
                              max_results=max_results, 
                              total_results=total_results, 
                              page_number=page_number 
        )
    )

def handle_food_description(food_desc: str) -> FoodModel.FoodDescription:
    serving, _, rest = food_desc.partition(" - ")
    serving = serving.strip()
    nutrition = [p.strip() for p in rest.split("|")] if rest else []
    info = {}
    for i in nutrition:
        key, _, value = i.partition(":")
        if key and value:
            info[key.strip().lower()] = value.strip()

    return FoodModel.FoodDescription(
        serving_size=serving,
        calories=info.get("calories", ""),
        fat=info.get("fat", ""),
        carbs=info.get("carbs", ""),
        protein=info.get("protein", ""),
    )