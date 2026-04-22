def validate_ingredients(ingredients: str) -> str:
    allowed = ["earth", "air", "fire", "water"]
    lower = ingredients.lower()
    for item in allowed:
        if item in lower:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
