import random


def gen_player_achievements() -> set:
    """Generates a random set of achievements for a player."""
    all_achievements = [
        "First Steps",
        "Master Explorer",
        "Treasure Hunter",
        "Boss Slayer",
        "Crafting Genius",
        "Survivor",
        "Speed Runner",
        "Hidden Path Finder",
        "Unstoppable",
        "Strategist",
        "World Savior",
        "Collector Supreme",
        "Sharp Mind"
    ]
    num_achievements = random.randint(1, len(all_achievements))
    return set(random.sample(all_achievements, num_achievements))


def main() -> None:
    """Achievement Tracker System demonstrating set operations."""
    print("=== Achievement Tracker System ===\n")

    players = [
        ("Alice", gen_player_achievements()),
        ("Bob", gen_player_achievements()),
        ("Charlie", gen_player_achievements()),
        ("Dylan", gen_player_achievements())
    ]

    for player in players:
        print(f"Player {player[0]}: {player[1]}")

    all_unique: set[str] = set()
    for player in players:
        all_unique = all_unique.union(player[1])

    print("\nAll distinct achievements:", all_unique)

    common_achievements: set[str] = set()
    for player in players:
        if not common_achievements:
            common_achievements = player[1]
        else:
            common_achievements = common_achievements.intersection(player[1])

    print("\nCommon achievements:", common_achievements)

    alice_achievements = players[0][1]
    bob_achievements = players[1][1]
    charlie_achievements = players[2][1]
    dylan_achievements = players[3][1]

    alice_unique = alice_achievements.difference(
        bob_achievements, charlie_achievements, dylan_achievements)
    bob_unique = bob_achievements.difference(
        alice_achievements, charlie_achievements, dylan_achievements)
    charlie_unique = charlie_achievements.difference(
        alice_achievements, bob_achievements, dylan_achievements)
    dylan_unique = dylan_achievements.difference(
        alice_achievements, bob_achievements, charlie_achievements)

    print("\nOnly Alice has:", alice_unique)
    print("Only Bob has:", bob_unique)
    print("Only Charlie has:", charlie_unique)
    print("Only Dylan has:", dylan_unique)

    alice_missing = all_unique.difference(alice_achievements)
    bob_missing = all_unique.difference(bob_achievements)
    charlie_missing = all_unique.difference(charlie_achievements)
    dylan_missing = all_unique.difference(dylan_achievements)

    print("\nAlice is missing:", alice_missing)
    print("Bob is missing:", bob_missing)
    print("Charlie is missing:", charlie_missing)
    print("Dylan is missing:", dylan_missing)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
