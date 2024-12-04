import collections

example: str = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def main(input: str) -> str:
    left, right = zip(
        *[[int(n) for n in line.split()] for line in input.splitlines() if line.strip()]
    )
    p1 = sum(abs(l - r) for (l, r) in zip(sorted(left), sorted(right)))
    c = collections.Counter(right)
    p2 = sum(n * c.get(n, 0) for n in left)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_that_day_01_works():
    assert main(example) == "Part 1: 11, Part 2: 31"
