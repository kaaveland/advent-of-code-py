from typing import Optional
from collections import defaultdict

example: str = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


class Grid:
    def __init__(self, s: str):
        lines = s.splitlines()
        self.height = len(lines)
        self.grid = "".join(lines)
        self.width = len(lines[0])

    def __contains__(self, ix: tuple[int, int]) -> bool:
        x, y = ix
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, ix: tuple[int, int]) -> Optional[int]:
        if ix in self:
            x, y = ix
            return ord(self.grid[y * self.width + x]) - ord("0")
        else:
            return None

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self.get((x, y))

    @property
    def trailheads(self):
        for x, y, v in self:
            if v == 0:
                yield x, y


def trail_metrics(grid: Grid, trailhead: tuple[int, int]) -> tuple[int, int]:
    visited = defaultdict(int)
    work = [trailhead]
    while work:
        x, y = work.pop()
        here = grid.get((x, y))
        visited[(x, y)] += 1
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid and grid.get((nx, ny)) == here + 1:
                work.append((nx, ny))
    score = sum(grid.get((x, y)) == 9 for x, y in visited)
    rating = sum(v for (x, y), v in visited.items() if grid.get((x, y)) == 9)
    return score, rating


def main(inp: str) -> str:
    grid = Grid(inp)
    p1 = p2 = 0
    for trailhead in grid.trailheads:
        score, rating = trail_metrics(grid, trailhead)
        p1 += score
        p2 += rating
    return f"Part 1: {p1}, Part 2: {p2}"


def test_day_10():
    assert main(example) == "Part 1: 36, Part 2: 81"
