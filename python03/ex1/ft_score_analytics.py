#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Player Score Analytics ===")

    args = sys.argv[1:]

    if len(args) == 0:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    scores = []

    for value in args:
        try:
            number = int(value)
            scores.append(number)
        except ValueError:
            print(f"Invalid parameter: '{value}'")

    if len(scores) == 0:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    total = sum(scores)
    average = total / len(scores)
    maximum = max(scores)
    minimum = min(scores)
    score_range = maximum - minimum

    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {average}")
    print(f"High score: {maximum}")
    print(f"Low score: {minimum}")
    print(f"Score range: {score_range}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
