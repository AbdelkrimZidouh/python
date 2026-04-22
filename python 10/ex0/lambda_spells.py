def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda it: it.get("power", 0), reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x.get("power", 0) >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda word: f"* {word} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    power_list = list(map(lambda m: m.get("power", 0), mages))

    return {
        "max_power": max(power_list),
        "min_power": min(power_list),
        "avg_power": round(sum(power_list) / len(power_list), 2)
    }


def main() -> None:
    print("\nTesting artifact sorter...")
    items = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"}
    ]
    ordered = artifact_sorter(items)
    if len(ordered) >= 2:
        print(f"{ordered[0]['name']} ({ordered[0]['power']} power) "
              f"comes before {ordered[1]['name']} "
              f"({ordered[1]['power']} power)")

    print("\nTesting spell transformer...")
    magic_words = ["fireball", "heal", "shield"]
    print(" ".join(spell_transformer(magic_words)))


if __name__ == "__main__":
    main()
