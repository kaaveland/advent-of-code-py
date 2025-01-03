import re

example: str = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

digits = re.compile(r"(\d+)")


def parse(inp: str):
    out = []
    for eq in inp.split("\n\n"):
        a_x, a_y, b_x, b_y, prize_x, prize_y = [int(m) for m in digits.findall(eq)]
        out.append((a_x, a_y, b_x, b_y, prize_x, prize_y))
    return out


def solve_eq(a_x, a_y, b_x, b_y, prize_x, prize_y):
    assert a_x * b_y - b_x * a_y != 0
    a = (prize_x * b_y - b_x * prize_y) // (a_x * b_y - b_x * a_y)
    b = (a_x * prize_y - prize_x * a_y) // (a_x * b_y - b_x * a_y)
    if a * a_x + b * b_x == prize_x and a * a_y + b * b_y == prize_y:
        return a, b
    else:
        return None, None


def main(inp: str) -> str:
    eqs = parse(inp)
    tokens = 0
    for eq in eqs:
        a, b = solve_eq(*eq)
        if a is not None and (a <= 100 and b <= 100):
            tokens += 3 * a + b
    p2_tokens = 0
    for eq in eqs:
        a_x, a_y, b_x, b_y, prize_x, prize_y = eq
        prize_x += 10000000000000
        prize_y += 10000000000000
        a, b = solve_eq(a_x, a_y, b_x, b_y, prize_x, prize_y)
        if a is not None:
            p2_tokens += 3 * a + b
    return f"Part 1: {tokens}, Part 2: {p2_tokens}"


def test_parse():
    assert parse(example) == [
        (94, 34, 22, 67, 8400, 5400),
        (26, 66, 67, 21, 12748, 12176),
        (17, 86, 84, 37, 7870, 6450),
        (69, 23, 27, 71, 18641, 10279),
    ]


def test_solve():
    assert solve_eq(94, 34, 22, 67, 8400, 5400) == (80, 40)
    assert solve_eq(26, 66, 67, 21, 12748, 12176) == (None, None)


def test_example():
    assert main(example).startswith("Part 1: 480")
