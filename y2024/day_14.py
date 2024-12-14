import re
from typing import Iterable, Optional
from math import prod

example: str = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def parse(input: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    pattern = re.compile(r"-?\d+")

    def parse(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
        p_x, p_y, v_x, v_y = [int(n) for n in pattern.findall(line)]
        return (p_x, p_y), (v_x, v_y)

    return [parse(line) for line in input.splitlines() if line.strip()]


def positions(
    bots: list[tuple[tuple[int, int], tuple[int, int]]],
    time: int,
    width: int,
    height: int,
) -> Iterable[tuple[int, int]]:
    return (
        ((px + vx * time) % width, (py + vy * time) % height)
        for (px, py), (vx, vy) in bots
    )


def safety_score(positions: Iterable[tuple[int, int]], width: int, height: int) -> int:
    scores = [0 for _ in range(4)]
    assert width % 2 == 1
    assert height % 2 == 1
    xmid = width // 2
    ymid = height // 2

    for x, y in positions:
        if x != xmid and y != ymid:
            qx = x // (xmid + 1)
            qy = y // (ymid + 1)
            scores[qx + qy * 2] += 1
    return prod(scores)


def christmas_tree(
    bots: list[tuple[tuple[int, int], tuple[int, int]]], width: int, height: int
) -> Optional[int]:
    for time in range(width * height):
        pos = set(positions(bots, time, width, height))
        if len(pos) == len(bots):
            return time
    return None


def main(input: str) -> str:
    bots = parse(input)
    width = 101
    height = 103
    p1 = safety_score(
        positions(bots, 100, width=width, height=height), width=width, height=height
    )
    p2 = christmas_tree(bots, width, height)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_part1():
    bots = parse(example)
    pos = positions(bots, 100, width=11, height=7)
    assert safety_score(pos, width=11, height=7) == 12


def test_positions():
    pos = positions([((2, 4), (2, -3))], 5, width=11, height=7)
    assert list(pos) == [(1, 3)]


def test_parse():
    bots = parse(example)
    assert bots[0] == ((0, 4), (3, -3))
    assert bots[-1] == ((9, 5), (-3, -3))
