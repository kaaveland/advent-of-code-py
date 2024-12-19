import functools

example: str = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def parse(inp: str) -> (tuple[str], list[str]):
    first, second = inp.split("\n\n")
    return (
        tuple(first.split(", ")),
        [line.strip() for line in second.splitlines() if line.strip()],
    )


def main(inp: str) -> str:
    towels, orders = parse(inp)

    @functools.cache
    def can_make(order: str) -> bool:
        if not order:
            return True
        else:
            return any(
                can_make(order[len(towel) :])
                for towel in towels
                if order.startswith(towel)
            )

    @functools.cache
    def possible_arrangements(order: str) -> int:
        if not order:
            return 1
        else:
            return sum(
                possible_arrangements(order[len(towel) :])
                for towel in towels
                if order.startswith(towel)
            )

    p1 = sum(can_make(o) for o in orders)
    p2 = sum(possible_arrangements(o) for o in orders)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_example():
    assert main(example) == "Part 1: 6, Part 2: 16"
