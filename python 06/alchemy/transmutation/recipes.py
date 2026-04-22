from alchemy.potions import strength_potion      # absolute import
from ..elements import create_air               # relative import
from elements import create_fire


def lead_to_gold() -> str:
    return (
        f"Recipe transmuting Lead to Gold: brew '{create_air()}'"
        f" and '{strength_potion()}'"
        f" mixed with '{create_fire()}'\n"
    )
