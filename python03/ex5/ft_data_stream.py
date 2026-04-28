import random
import typing


def gen_event() -> typing.Generator:
    players = ['alice', 'bob', 'charlie', 'dylan']
    actions = [
        'run', 'eat', 'sleep', 'grab', 'move',
        'climb', 'swim', 'use', 'release'
    ]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(event_list: list) -> typing.Generator:
    while len(event_list) > 0:
        event = random.choice(event_list)
        event_list.remove(event)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    gen = gen_event()
    for i in range(1000):
        event = next(gen)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    gen2 = gen_event()
    event_list = []
    for _ in range(10):
        event_list.append(next(gen2))
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
