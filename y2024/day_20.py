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
) -> tuple[dict[int, int], dict[Pos, Optional[Pos]]]:
    distances = defaultdict(lambda: sys.maxsize)
    parents = {}
    work: deque[tuple[tuple[int, int], int, Optional[tuple[int, int]]]] = deque(
        [(pos, 0, None)]
    )
    visited = set()
    while work:
        (x, y), distance, parent = work.popleft()
        if not (x, y) in visited and maze.get((x, y), False):
            distances[(x & 0xFF) | ((y & 0xFF) << 8)] = distance

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


def manhattan_offsets(cheat_len: int) -> list[tuple[int, int, int]]:
    offsets = []
    for dx in range(-cheat_len, cheat_len + 1):
        max_dy = cheat_len - abs(dx)
        for dy in range(-max_dy, max_dy + 1):
            offsets.append((dx, dy, abs(dx) + abs(dy)))
    return offsets


def find_cheats(
    dist: dict[int, int], path: list[Pos], cheat_len: int, mingain: int
) -> int:
    cheats: int = 0
    offsets = manhattan_offsets(cheat_len)
    for x, y in path:
        remaining = dist[(x & 0xFF) | ((y & 0xFF) << 8)]
        for dx, dy, cost in offsets:
            nx, ny = x + dx, y + dy
            gain = dist.get((nx & 0xFF) | ((ny & 0xFF) << 8), -1000) - cost - remaining
            if gain >= mingain:
                cheats += 1
    return cheats


def main(inp: str) -> str:
    m = maze(inp)
    start, end = find_match(inp, "S"), find_match(inp, "E")
    dist, parents = bfs(m, end)
    path = find_path(parents, start)

    p1 = find_cheats(dist, path, 2, 100)
    p2 = find_cheats(dist, path, 20, 100)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_bfs():
    m = maze(example)
    start, end = find_match(example, "S"), find_match(example, "E")
    (x, y) = start
    dist, parents = bfs(m, end)
    path = find_path(parents, start)
    assert dist[(x & 0xFF) | ((y & 0xFF) << 8)] == 84
    assert start in path and end in path
    assert len(path) == 85
