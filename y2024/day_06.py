example: str = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def resolve_segment(segment, cache, end_pos, end_dir):
    for seg_pos, seg_dir in segment:
        cache[(seg_pos, seg_dir)] = (end_pos, end_dir)


def build_path_cache(
    grid, pos
) -> dict[tuple[tuple[int, int], int], tuple[tuple[int, int], int]]:
    dir = 0
    cache: dict[tuple[tuple[int, int], int], tuple[tuple[int, int], int]] = {}
    segment_keys = []
    width, height = len(grid[0]), len(grid)

    while True:
        segment_keys.append((pos, dir))
        dx, dy = dirs[dir]
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny][nx] != "#":
                pos = nx, ny
            else:
                dir = (dir + 1) % 4
                # all positions in this segment up here
                resolve_segment(segment_keys, cache, pos, dir)
                segment_keys = []
        else:
            # The current segment ends outside the map
            resolve_segment(segment_keys, cache, (nx, ny), dir)
            return cache


def loops(grid, pos, cache, obs) -> bool:
    dir = 0
    visited = set()
    width, height = len(grid[0]), len(grid)
    while True:
        seen = (pos, dir) in visited
        visited.add((pos, dir))
        if seen:
            return True
        # Use the case if the new obstacle is not in this row or column
        elif (pos, dir) in cache and not (obs[0] == pos[0] or obs[1] == pos[1]):
            pos, dir = cache[(pos, dir)]
        else:
            dx, dy = dirs[dir]
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] != "#" and (nx, ny) != obs:
                    pos = nx, ny
                else:
                    dir = (dir + 1) % 4
            else:
                return False


def main(input: str) -> str:
    grid = [line.strip() for line in input.splitlines()]
    height, width = len(grid), len(grid[0])
    origin = (0, 0)
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "^":
                origin = x, y
                break
    cache = build_path_cache(grid, origin)
    path = {
        pos
        for pos, _ in cache
        if 0 <= pos[0] <= len(grid[0]) and 0 <= pos[1] < len(grid)
    }
    p1 = len(path)
    path.remove(origin)
    p2 = sum(loops(grid, origin, cache, obs) for obs in path)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_day_6():
    assert main(example) == "Part 1: 41, Part 2: 6"
