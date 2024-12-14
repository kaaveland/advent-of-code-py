import heapq

example: str = "2333133121414131402"


def parse(inp: str) -> list[int]:
    disk = []
    for i, ch in enumerate(inp):
        v = i // 2
        if i % 2 == 0:
            for _ in range(int(ch)):
                disk.append(v)
        else:
            for _ in range(int(ch)):
                disk.append(-1)
    return disk


def fragment_disk(disk: list[int]):
    fp = len(disk) - 1
    sp = 0
    while True:
        if sp >= fp or fp < 0 or sp > len(disk) - 1:
            break
        if disk[sp] != -1:
            sp += 1
        elif disk[fp] == -1:
            fp -= 1
        else:
            disk[sp], disk[fp] = disk[fp], disk[sp]
            sp += 1
            fp -= 1


def checksum(disk: list[int]):
    return sum(i * v for i, v in enumerate(disk) if v != -1)


def defragment_disk(disk: list[int]):
    # find space locations
    space_indexes: list[list[tuple[int, int]]] = [[] for _ in range(10)]
    i = 0
    start = None
    while i < len(disk):
        if disk[i] == -1 and start is None:
            start = i
        elif disk[i] != -1 and start is not None:
            end = i
            slot_size = end - start
            space_indexes[slot_size].append((start, end))
            start = None
        i += 1
    space_indexes = [index for index in space_indexes]
    for index in space_indexes:
        heapq.heapify(index)

    file_index = {}
    for i, v in enumerate(disk):
        if v != -1:
            file_index[v] = i

    for content, end in sorted(file_index.items(), reverse=True):
        start = end
        while start > 0 and disk[start] == content:
            start -= 1
        start += 1
        end += 1
        fsize = end - start
        try:
            chosen_heap = min(
                [h for h in space_indexes[fsize:] if h], key=lambda heap: heap[0]
            )
        except ValueError:
            continue  # No heap has room
        space_start, space_end = heapq.heappop(chosen_heap)
        if start < space_start:
            continue
        disk[space_start : space_start + fsize] = disk[start:end]
        disk[start:end] = [-1 for _ in range(fsize)]
        remaining = space_end - space_start - fsize
        if remaining:
            heapq.heappush(space_indexes[remaining], (space_start + fsize, space_end))


def main(inp: str) -> str:
    disk = parse(inp)
    fragment_disk(disk)
    p1 = checksum(disk)
    disk = parse(inp)
    defragment_disk(disk)
    p2 = checksum(disk)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_day_09():
    assert main(example) == "Part 1: 1928, Part 2: 2858"
