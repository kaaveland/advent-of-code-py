from collections import Counter


def main(inp: str) -> str:
    p1, counter = 0, Counter()
    for monkey in inp.splitlines():
        secret: int = int(monkey)
        last_price = secret % 10
        d1 = d2 = d3 = None
        seen = set()

        for i in range(2000):
            secret = ((secret << 6) ^ secret) & 0xFFFFFF
            secret = ((secret >> 5) ^ secret) & 0xFFFFFF
            secret = ((secret << 11) ^ secret) & 0xFFFFFF
            price = secret % 10
            (d0, d1, d2) = (d1, d2, d3)
            d3 = price - last_price + 9  # ensure min val is 0 to construct k
            if i >= 3:  # seen 4 prices
                k = (
                    (d0 & 0x1F)
                    | ((d1 & 0x1F) << 5)
                    | ((d2 & 0x1F) << 10)
                    | ((d3 & 0x1F) << 15)
                )
                if k not in seen:
                    seen.add(k)
                    counter[k] += price
            last_price = price
        p1 += secret

    p2 = max(counter.values())
    return f"Part 1: {p1}, Part 2: {p2}"
