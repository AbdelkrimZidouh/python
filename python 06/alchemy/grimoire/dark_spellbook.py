from .dark_validator import dark_validate_ingredients


def dark_spell_allowed_ingredients() -> list:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result = dark_validate_ingredients(ingredients)
    if "VALID" in result and "INVALID" not in result:
        return f"Dark spell recorded: {spell_name} ({result})"
    return f"Dark spell rejected: {spell_name} ({result})"
