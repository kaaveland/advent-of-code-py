from functools import cmp_to_key

example: str = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def main(input: str) -> str:
    rules, updates = input.split("\n\n")
    rules = {line.strip() for line in rules.split()}
    updates = [
        [int(n.strip()) for n in update.split(",")]
        for update in updates.splitlines()
        if update.strip()
    ]

    def cmp(left, right):
        if f"{left}|{right}" in rules:
            return -1
        elif f"{right}|{left}" in rules:
            return 1
        else:
            return 0

    total, total_wrong = 0, 0
    for update in updates:
        ordered = sorted(update, key=cmp_to_key(cmp))
        middle = ordered[int(len(ordered) / 2)]
        if update == ordered:
            total += middle
        else:
            total_wrong += middle
    return f"Part 1: {total}, Part 2: {total_wrong}"


def test_day_5():
    assert main(example) == "Part 1: 143, Part 2: 123"
