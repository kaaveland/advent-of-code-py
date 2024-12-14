from collections import defaultdict
from functools import partial
from itertools import islice, chain, combinations
from typing import Generator, Tuple, List, Iterable

example: str = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def parse(input: str) -> dict[str, List[Tuple[int, int]]]:
    out = defaultdict(list)
    for y, line in enumerate(input.splitlines()):
        for x, ch in enumerate(line):
            if ch != ".":
                out[ch].append((x, y))
    return out


def antinodes(
    antenna_1, antenna_2, height, width, dir=-1
) -> Generator[Tuple[int, int]]:
    x1, y1 = antenna_1
    x2, y2 = antenna_2
    dx, dy = x2 - x1, y2 - y1
    x, y = (x1, y1) if dir < 0 else (x2, y2)
    while 0 <= x < width and 0 <= y < height:
        yield x, y
        x += dir * dx
        y += dir * dy


def p1_antinodes(antenna_1, antenna_2, height, width) -> Iterable[Tuple[int, int]]:
    gen = partial(antinodes, antenna_1, antenna_2, height, width)
    return chain(islice(gen(dir=-1), 1, 2), islice(gen(dir=1), 1, 2))


def p2_antinodes(antenna_1, antenna_2, height, width) -> Iterable[Tuple[int, int]]:
    gen = partial(antinodes, antenna_1, antenna_2, height, width)
    return chain(gen(dir=-1), gen(dir=1))


def group_antinodes(
    group: list[Tuple[int, int]], generator
) -> Iterable[Tuple[int, int]]:
    return chain(*[generator(a, b) for a, b in combinations(group, 2)])


def main(input: str) -> str:
    height, width = len(input.splitlines()), len(input.splitlines()[0])
    antennas = parse(input)
    gen_p1 = partial(p1_antinodes, height=height, width=width)
    gen_p2 = partial(p2_antinodes, height=height, width=width)
    p1 = set(chain(*[group_antinodes(group, gen_p1) for group in antennas.values()]))
    p2 = set(chain(*[group_antinodes(group, gen_p2) for group in antennas.values()]))
    return f"Part 1: {len(p1)}, Part 2: {len(p2)}"


def test_day_8():
    assert main(example) == "Part 1: 14, Part 2: 34"
