from typing import Optional

import heapq

example: str = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def shortest_path(
    memory: list[tuple[int, int]],
    nanoseconds: int,
    start: tuple[int, int],
    end: tuple[int, int],
) -> Optional[int]:
    obstacles = {memory[i] for i in range(nanoseconds)}
    visited = set()
    xbounds = range(end[0] + 1)
    ybounds = range(end[1] + 1)
    work = [(0, start)]

    while work:
        cost, (x, y) = heapq.heappop(work)
        if (x, y) == end:
            return cost
        elif (x, y) in visited:
            continue
        else:
            visited.add((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if nx in xbounds and ny in ybounds and (nx, ny) not in obstacles:
                    heapq.heappush(work, (cost + 1, (nx, ny)))
    return None


def parse_memory(inp: str) -> list[tuple[int, int]]:
    memory = []
    for line in inp.splitlines():
        if line:
            x, y = line.split(",")
            memory.append((int(x), int(y)))
    return memory


def main(inp: str) -> str:
    memory = parse_memory(inp)
    p1 = shortest_path(memory, 1024, (0, 0), (70, 70))

    bot = 1024
    top = len(memory)

    while bot < top:
        mid = bot + (top - bot) // 2
        if shortest_path(memory, mid, (0, 0), (70, 70)) is None:
            top = mid
        else:
            bot = mid + 1

    return f"Part 1: {p1}, Part 2: {memory[bot - 1]}"


def test_p1():
    memory = parse_memory(example)
    assert shortest_path(memory, 12, (0, 0), (6, 6)) == 22
