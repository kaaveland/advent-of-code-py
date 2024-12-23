from collections import Counter


def main(inp: str) -> str:
    p1, counter = 0, Counter()
    k_mask = (1 << 20) - 1
    for monkey in inp.splitlines():
        secret: int = int(monkey)
        last_price = secret % 10
        k = 0
        seen = set()

        for i in range(2000):
            secret = ((secret << 6) ^ secret) & 0xFFFFFF
            secret = ((secret >> 5) ^ secret) & 0xFFFFFF
            secret = ((secret << 11) ^ secret) & 0xFFFFFF
            price = secret % 10
            k = ((k << 5) | (price - last_price + 9) & 0x1F) & k_mask
            if i >= 3:  # seen 4 prices
                if k not in seen:
                    seen.add(k)
                    counter[k] += price
            last_price = price
        p1 += secret

    p2 = max(counter.values())
    return f"Part 1: {p1}, Part 2: {p2}"
