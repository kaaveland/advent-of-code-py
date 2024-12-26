def main(s: str) -> str:
    blocks = s.split("\n\n")
    keys: list[set[tuple[int, int]]] = []
    locks: list[set[tuple[int, int]]] = []
    for block in blocks:
        dest = locks if block.startswith("#") else keys
        dest.append(
            {
                (x, y)
                for y, line in enumerate(block.splitlines())
                for x, ch in enumerate(line)
                if ch == "#"
            }
        )
    could_fit = 0
    for key in keys:
        for lock in locks:
            if not key & lock:
                could_fit += 1
    return f"Part 1: {could_fit}, Part 2: Collect stars"
