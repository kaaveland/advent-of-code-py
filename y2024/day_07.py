from operator import mul, add
from math import log10

example: str = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def conc(left, right):
    exp = int(log10(right)) + 1
    return int(left * (10**exp) + right)


def main(input: str) -> str:
    equations = [
        (int(l.split(":")[0]), [int(n) for n in l.split(":")[1].split()])
        for l in input.splitlines()
        if l.strip()
    ]

    def reduces(left, rest, target, ops):
        if left > target:
            return False
        elif not rest:
            return left == target
        else:
            return any(reduces(op(left, rest[0]), rest[1:], target, ops) for op in ops)

    p1 = sum(
        target
        for target, operands in equations
        if reduces(operands[0], operands[1:], target, ops=[mul, add])
    )
    p2 = sum(
        target
        for target, operands in equations
        if reduces(operands[0], operands[1:], target, ops=[mul, add, conc])
    )
    return f"Part 1: {p1}, Part 2: {p2}"


def test_conc():
    assert conc(12, 345) == 12345


def test_day_07():
    assert main(example) == "Part 1: 3749, Part 2: 11387"
