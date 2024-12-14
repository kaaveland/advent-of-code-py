from typing import Optional

example: str = """AAAA
BBCD
BBCC
EEEC
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

    def get(self, ix: tuple[int, int]) -> Optional[str]:
        if ix in self:
            x, y = ix
            return self.grid[y * self.width + x]
        else:
            return None

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self.get((x, y))


def perimeter_by_area(grid: Grid) -> int:
    claimed = set()
    work = list(grid)
    price = 0
    while work:
        x, y, here = work.pop()
        area = perimeter = 0
        inner = [(x, y, here)]
        while inner:
            x, y, here = inner.pop()
            if (x, y) in claimed:
                continue
            claimed.add((x, y))
            area += 1
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if grid.get((nx, ny)) != here:
                    perimeter += 1
                if (nx, ny) in grid and grid.get((nx, ny)) == here:
                    inner.append((nx, ny, here))
        price += area * perimeter
    return price


def sides_by_area(grid: Grid) -> int:
    claimed = set()
    work = list(grid)
    price = 0
    while work:
        x, y, here = work.pop()
        area = sides = 0
        inner = [(x, y, here)]
        while inner:
            x, y, here = inner.pop()
            if (x, y) in claimed:
                continue
            claimed.add((x, y))
            area += 1
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                v = grid.get((nx, ny))
                if v == here:
                    inner.append((nx, ny, v))
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                horizontal = grid.get((x + dx, y))
                vertical = grid.get((x, y + dy))
                diagonal = grid.get((x + dx, y + dy))
                if (here != horizontal and here != vertical) or (
                    here == horizontal and here == vertical and here != diagonal
                ):
                    sides += 1
        price += area * sides
    return price


def main(inp: str) -> str:
    grid = Grid(inp)
    p1 = perimeter_by_area(grid)
    p2 = sides_by_area(grid)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_perimeter_by_area():
    grid = Grid(example)
    assert perimeter_by_area(grid) == 140


def test_sides_by_area():
    grid = Grid(example)
    assert sides_by_area(grid) == 80
