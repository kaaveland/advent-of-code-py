from collections import defaultdict
from itertools import combinations

example: str = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def parse(inp: str) -> defaultdict[str, set[str]]:
    d = defaultdict(set)
    for line in inp.splitlines():
        a, b = line.split("-")
        d[a].add(b)
        d[b].add(a)
    return d


def max_clique(nodes: set[str], graph: dict[str, set[str]]) -> set[str]:
    if len(nodes) in (0, 1):
        return nodes
    temp = set(nodes)
    node = temp.pop()
    with_, without = (max_clique(graph[node] & temp, graph) | {node}), max_clique(
        temp, graph
    )
    return with_ if len(with_) > len(without) else without


def main(inp: str) -> str:
    network = parse(inp)
    found = set()
    for k, v in network.items():
        if not k.startswith("t"):
            continue
        for a, b in combinations(v, 2):
            # we know that k is in network[a] and network[b] trivially
            if a in network[b] and b in network[a]:
                found.add(frozenset({k, a, b}))
    p1 = len(found)

    current_best = max_clique(set(network.keys()), network)
    p2 = ",".join(sorted(current_best))
    return f"Part 1: {p1}, Part 2: {p2}"


def test_p1():
    assert main(example) == "Part 1: 7, Part 2: co,de,ka,ta"
