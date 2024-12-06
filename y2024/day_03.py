import re

example = (
    """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
)


def main(input: str) -> str:
    dodontmul = re.compile(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))")
    mul_enabled = True
    p1, p2 = 0, 0
    for m in dodontmul.findall(input):
        mul, l, r, do, dont = m
        if dont:
            mul_enabled = False
        elif do:
            mul_enabled = True
        elif mul:
            p1 += int(l) * int(r)
            if mul_enabled:
                p2 += int(l) * int(r)
    return f"Part 1: {p1}, Part 2: {p2}"


def test_example():
    assert main(example) == "Part 1: 161, Part 2: 48"
