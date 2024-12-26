from collections import defaultdict, deque


def parse(s: str) -> tuple[dict[str, bool], dict[str, tuple[str, str, str]]]:
    provided, calculated = s.split("\n\n")
    known = {line.split(": ")[0]: line.endswith("1") for line in provided.splitlines()}
    ops = {}
    for line in calculated.splitlines():
        if line.strip():
            (lhs, op, rhs, _, dest) = line.split()
            ops[dest] = (op, lhs, rhs)
    return known, ops


def calculate(
    known: dict[str, bool], calculated: dict[str, tuple[str, str, str]]
) -> int:
    depends_on = defaultdict(list)
    for wire, (op, lhs, rhs) in calculated.items():
        depends_on[lhs].append(wire)
        depends_on[rhs].append(wire)
    # Signals that are set
    wires = known.copy()
    # Signals we need to propagate
    work = deque([w for w in wires])
    while work:
        current = work.popleft()
        if current in wires:
            for next_op in depends_on[current]:
                (op, lhs, rhs) = calculated[next_op]
                if lhs in wires and rhs in wires:
                    if op == "XOR":
                        wires[next_op] = wires[lhs] ^ wires[rhs]
                    elif op == "OR":
                        wires[next_op] = wires[lhs] | wires[rhs]
                    elif op == "AND":
                        wires[next_op] = wires[lhs] & wires[rhs]
                    work.append(next_op)
    return sum(
        val << i
        for i, (wire, val) in enumerate(
            sorted([(k, v) for k, v in wires.items() if k.startswith("z")])
        )
    )


def identify_bad_gates(calculated: dict[str, tuple[str, str, str]]) -> set[str]:
    sus = set()
    for wire, (op, lhs, rhs) in calculated.items():
        # z should be all XOR, except highest, which is permitted to be OR
        if op != "XOR" and wire.startswith("z") and wire != "z45":
            sus.add(wire)
        # if z is not XOR, what was it swapped with? Probably doing carry-out
        # which looks like: ((x ^ y) & carry-in) | (x & y)
        # So let's look for a XOR where we should get an OR
        # All XOR should produce z _or_ use x and y
        if (
            op == "XOR"
            and not lhs[0] in "xy"
            and not rhs[0] in "xy"
            and not wire.startswith("z")
        ):
            sus.add(wire)
        depends_on = {
            next_op
            for next_op, next_lhs, next_rhs in calculated.values()
            if next_lhs == wire or next_rhs == wire
        }
        # Other than the initial carry bit, AND should provide to OR
        if op == "AND" and lhs != "x00" and rhs != "y00":
            if depends_on != {"OR"}:
                sus.add(wire)
        # Swapped with the above
        if op == "XOR" and "OR" in depends_on:
            sus.add(wire)
    return sus


def main(inp: str) -> str:
    known, calculated = parse(inp)
    p1 = calculate(known, calculated)
    p2 = sorted(identify_bad_gates(calculated))
    return f"Part 1: {p1}, Part 2: {','.join(p2)}"
