from math import log10

# import numba
# import numba.typed

example: str = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


# @numba.jit(
#    numba.int64(numba.int64, numba.int64), nopython=True, cache=True, fastmath=True
# )
def conc(left: int, right: int) -> int:
    exp = int(log10(right)) + 1
    return int(left * (10**exp) + right)


# @numba.jit(cache=True, nopython=True, fastmath=True)
def reduces(operands: list[int], target: int, include_conc: bool = False) -> bool:
    head, tail = operands[0], operands[1:]
    work: list[tuple[int, list[int]]] = [(head, tail)]
    while work:
        head, tail = work.pop()
        if head > target:
            continue
        elif not tail and head == target:
            return True
        elif tail:
            ntail = tail[1:]
            work.append((head * tail[0], ntail))
            work.append((head + tail[0], ntail))
            if include_conc:
                work.append((conc(head, tail[0]), ntail))
    return False


def main(input: str) -> str:
    equations = [
        (int(l.split(":")[0]), [int(n) for n in l.split(":")[1].split()])
        for l in input.splitlines()
        if l.strip()
    ]

    p1_ans = [
        (i, target)
        for i, (target, operands) in enumerate(equations)
        if reduces(operands, target, False)
    ]
    p1_solved = {i for i, _ in p1_ans}

    p1 = sum(target for _, target in p1_ans)
    p2 = sum(
        target
        for i, (target, operands) in enumerate(equations)
        if i in p1_solved or reduces(operands, target, True)
    )
    return f"Part 1: {p1}, Part 2: {p2}"


def test_conc():
    assert conc(12, 345) == 12345


def test_day_07():
    assert main(example) == "Part 1: 3749, Part 2: 11387"
