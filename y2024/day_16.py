from typing import TypeAlias
import heapq
import sys

example: str = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

Pos: TypeAlias = tuple[int, int]
Maze: TypeAlias = set[Pos]
State: TypeAlias = tuple[int, Pos, int]
Cache: TypeAlias = dict[tuple[Pos, int], int]


def parse(inp: str) -> tuple[Maze, Pos, Pos]:
    maze: Maze = set()
    start: Pos = (0, 0)
    end: Pos = (0, 0)
    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                maze.add((x, y))
            elif c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
    assert start != (0, 0)
    assert end != (0, 0)
    assert start != end
    return maze, start, end


DIRS: list[Pos] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def step(pos: Pos, dir: int) -> Pos:
    x, y = pos
    dx, dy = DIRS[dir]
    return x + dx, y + dy


def solve(maze: Maze, start: Pos, end: Pos) -> tuple[int, Cache]:
    cache: Cache = {}
    work = [(0, start, 1)]
    while work:
        cost, pos, dir = heapq.heappop(work)
        if pos == end:
            return cost, cache
        next_states = [
            (cost + 1, step(pos, dir), dir),
            (cost + 1000, pos, (dir + 1) % 4),
            (cost + 1000, pos, (dir - 1) % 4),
        ]
        for next_cost, next_pos, next_dir in next_states:
            if (
                next_cost < cache.get((next_pos, next_dir), sys.maxsize)
                and next_pos not in maze
            ):
                cache[(next_pos, next_dir)] = next_cost
                heapq.heappush(work, (next_cost, next_pos, next_dir))
    raise ValueError("No solution found")


def main(inp: str) -> str:
    maze, start, end = parse(inp)
    p1, cache = solve(maze, start, end)
    end_dir = [i for i in range(4) if (end, i) in cache][0]
    visited = set()
    work = [(p1, end, end_dir)]
    while work:
        cost, pos, dir = work.pop()
        visited.add(pos)
        possible_parents = [
            (cost - 1, step(pos, (dir + 2) % 4), dir),
            (cost - 1000, pos, (dir + 1) % 4),
            (cost - 1000, pos, (dir - 1) % 4),
        ]
        for parent_cost, parent_pos, parent_dir in possible_parents:
            if cache.get((parent_pos, parent_dir)) == parent_cost:
                work.append((parent_cost, parent_pos, parent_dir))

    return f"Part 1: {p1}, Part 2: {len(visited)}"


def test_solve_example():
    assert main(example) == "Part 1: 7036, Part 2: 45"
