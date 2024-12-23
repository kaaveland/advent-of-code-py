from collections import deque
from itertools import product, chain, pairwise
from functools import cache

KEYPAD: str = """789
456
123
#0A"""

DIRPAD: str = """#^A
<v>"""

DIRS: list[tuple[str, tuple[int, int]]] = [
    ("v", (0, 1)),
    ("^", (0, -1)),
    ("<", (-1, 0)),
    (">", (1, 0)),
]


def neighbour_list(inp: str) -> dict[str, list[tuple[str, str]]]:
    chmap = {
        (x, y): ch
        for y, line in enumerate(inp.splitlines())
        for x, ch in enumerate(line)
        if ch != "#"
    }
    neighours: dict[str, list[tuple[str, str]]] = {}
    for (x, y), ch in chmap.items():
        for d, (dx, dy) in DIRS:
            nx, ny = x + dx, y + dy
            neighbour = chmap.get((nx, ny))
            if neighbour is not None:
                neighours.setdefault(ch, []).append((neighbour, d))
    return neighours


def shortest_paths(
    neighbour_list: dict[str, list[tuple[str, str]]], start: str, end: str
) -> list[str]:
    work = deque([(start, "")])
    paths = []
    found = False
    path_len = 0

    while work:
        pos, path = work.popleft()
        if found and len(path) > path_len:
            break
        elif pos == end:
            found = True
            paths.append(path)
            path_len = len(path)
        else:
            for n, dir in neighbour_list[pos]:
                new_path = path + dir
                work.append((n, new_path))
    return paths


def all_pairs_shortest_paths(
    neighbour_list: dict[str, list[tuple[str, str]]]
) -> dict[tuple[str, str], list[str]]:
    return {
        (a, b): shortest_paths(neighbour_list, a, b)
        for a, b in product(neighbour_list, neighbour_list)
    }


def min_keypresses(
    depth: int,
    desired_output: str,
    keypad: dict[tuple[str, str], list[str]],
    dirpad: dict[tuple[str, str], list[str]],
) -> int:
    @cache
    def inner(depth: int, desired_output: str, use_keypad: bool):
        chars = chain("A", desired_output)
        pad = keypad if use_keypad else dirpad
        cost = []
        for first, then in pairwise(chars):
            shortest_paths = pad[(first, then)]
            if depth == 0:
                cost.append(len(shortest_paths[0]) + 1)
            else:
                cost.append(
                    min(inner(depth - 1, path + "A", False) for path in shortest_paths)
                )
        return sum(cost)

    return inner(depth, desired_output, True)


def complexity_score(
    code: str,
    depth: int,
    keypad: dict[tuple[str, str], list[str]],
    dirpad: dict[tuple[str, str], list[str]],
):
    presses = min_keypresses(depth, code, keypad, dirpad)
    code_no = int(code[:-1])
    return presses * code_no


def main(inp: str) -> str:
    keypad = all_pairs_shortest_paths(neighbour_list(KEYPAD))
    dirpad = all_pairs_shortest_paths(neighbour_list(DIRPAD))

    p1 = sum(
        complexity_score(code, 2, keypad, dirpad)
        for code in inp.splitlines()
        if code.strip()
    )
    p2 = sum(
        complexity_score(code, 25, keypad, dirpad)
        for code in inp.splitlines()
        if code.strip()
    )
    return f"Part 1: {p1}, Part 2: {p2}"
