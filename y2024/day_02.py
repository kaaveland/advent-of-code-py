example: str = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def main(inp: str) -> str:
    reports = [
        [int(n) for n in line.split()]
        for line in inp.splitlines()
    ]
    p1 = len([r for r in reports if safe(r)])
    p2 = len([r for r in reports if safe_with_removal(r)])
    return f"Part 1: {p1}, Part 2: {p2}"


def sign(n):
    return (n > 0) - (n < 0)


def safe(report):
    pairs = [l - r for (l, r) in zip(report, report[1:])]
    signs = set([sign(n) for n in pairs])
    maxdiff = max(abs(n) for n in pairs)
    return (signs == {-1} or signs == {1}) and maxdiff <= 3


def safe_with_removal(report):
    return any(
        safe(r) for r in
        [report[:i] + report[i + 1 :] for i in range(len(report))]
    )


def test_day_02():
    assert main(example) == "Part 1: 2, Part 2: 4"
