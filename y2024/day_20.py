from collections import deque, defaultdict
from typing import Iterator, Optional, TypeAlias
import sys

example: str = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


Pos: TypeAlias = tuple[int, int]


def parse_maze(inp: str) -> Iterator[tuple[int, int, str]]:
    for y, line in enumerate(inp.splitlines()):
        for x, ch in enumerate(line):
            yield x, y, ch


def maze(inp: str) -> dict[Pos, bool]:
    return {(x, y): ch in ".ES" for x, y, ch in parse_maze(inp)}


def find_match(inp: str, lookfor: str) -> Pos:
    for x, y, ch in parse_maze(inp):
        if ch == lookfor:
            return x, y
    raise ValueError(f"{lookfor} not found")


def bfs(
    maze: dict[Pos, bool], pos: Pos
) -> tuple[dict[Pos, int], dict[Pos, Optional[Pos]]]:
    distances = defaultdict(lambda: sys.maxsize)
    parents = {}
    work: deque[tuple[tuple[int, int], int, Optional[tuple[int, int]]]] = deque(
        [(pos, 0, None)]
    )
    visited = set()
    while work:
        (x, y), distance, parent = work.popleft()
        if not (x, y) in visited and maze.get((x, y), False):
            distances[(x, y)] = distance

            parents[(x, y)] = parent
            visited.add((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                work.append(((nx, ny), distance + 1, (x, y)))
    return distances, parents


def find_path(parents: dict[Pos, Optional[Pos]], pos: Pos) -> list[Pos]:
    path = [pos]
    cur: Optional[Pos] = pos
    while cur is not None and (cur := parents.get(cur)):
        if cur is not None:
            path.append(cur)
    return path


def manhattan(left: Pos, right: Pos) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def find_cheats(inp: str, cheat_len: int) -> dict[int, int]:
    m = maze(inp)
    start, end = find_match(inp, "S"), find_match(inp, "E")
    dist, parents = bfs(m, end)
    cheats: dict[int, int] = defaultdict(int)

    for x, y in find_path(parents, start):
        remaining = dist[(x, y)]
        for dx in range(-cheat_len, cheat_len + 1):
            allowed_dy = cheat_len - abs(dx)
            for dy in range(-allowed_dy, allowed_dy + 1):
                nx, ny = x + dx, y + dy
                if m.get((nx, ny)):
                    cost = manhattan((nx, ny), (x, y))
                    gain = remaining - dist[(nx, ny)] + cost
                    cheats[-gain] += 1
    return cheats


def main(inp: str) -> str:
    p1 = sum(count for gain, count in find_cheats(inp, 2).items() if gain >= 100)
    p2 = sum(count for gain, count in find_cheats(inp, 20).items() if gain >= 100)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_bfs():
    m = maze(example)
    start, end = find_match(example, "S"), find_match(example, "E")
    dist, parents = bfs(m, end)
    path = find_path(parents, start)
    assert dist[start] == 84
    assert start in path and end in path
    assert len(path) == 85
