import re
from collections import deque
from typing import Iterable, Iterator


def run_program(
    program: list[int], reg_a: int, reg_b: int, reg_c: int, ip: int = 0
) -> Iterator[int]:
    while ip < len(program):
        jmp = False
        op, operand = program[ip : ip + 2]
        operand = (
            {
                4: reg_a,
                5: reg_b,
                6: reg_c,
            }.get(operand, operand)
            if op in {0, 6, 7, 2, 5}
            else operand
        )
        if op == 0:  # adv
            reg_a = reg_a // (2**operand)
        elif op == 1:  # bxl
            reg_b ^= operand
        elif op == 2:  # bst
            reg_b = operand % 8
        elif op == 3:  # jnz
            if reg_a != 0:
                ip = operand
                jmp = True
        elif op == 4:  # bxc
            reg_b ^= reg_c
        elif op == 5:  # out
            yield operand % 8
        elif op == 6:  # bdv
            reg_b = reg_a // (2**operand)
        elif op == 7:  # cdv
            reg_c = reg_a // (2**operand)
        else:
            raise ValueError(f"Invalid op: {op}")

        if not jmp:
            ip += 2


def main(inp: str) -> str:
    prog_re = re.compile(
        r"""^Register A: (\d+)
Register B: (\d+)
Register C: (\d+)

Program: (.+)$"""
    )
    m = prog_re.match(inp)
    reg_a, reg_b, reg_c, prog = m.group(1), m.group(2), m.group(3), m.group(4)
    prog = [int(n) for n in prog.split(",")]
    out = run_program(prog, int(reg_a), int(reg_b), int(reg_c))
    p1 = ",".join(str(n) for n in out)

    work = deque([0])

    for require in reversed(prog):
        for _ in range(len(work)):
            current = work.popleft()

            for octet in range(8):
                search = (current << 3) | octet
                if next(run_program(prog, search, 0, 0)) == require:
                    work.append(search)

    p2 = work.popleft()
    return f"Part 1: {p1}, Part 2: {p2}"


def test_example_1():
    prog = [0, 1, 5, 4, 3, 0]
    assert list(run_program(prog, 729, 0, 0)) == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]
