from collections import Counter


def main(inp: str) -> str:
    p1 = 0
    k_range = 19**4
    counter: Counter[int] = Counter()
    s_mask = 0xFFFFFF
    for monkey in inp.splitlines():
        secret: int = int(monkey)
        last_price = secret % 10
        k = 0
        seen = set()

        for i in range(2000):
            secret = ((secret << 6) ^ secret) & s_mask
            secret = ((secret >> 5) ^ secret) & s_mask
            secret = ((secret << 11) ^ secret) & s_mask
            price = secret % 10
            k = (k * 19 + price - last_price + 9) % k_range
            if i >= 3:  # seen 4 prices
                if k not in seen:
                    seen.add(k)
                    counter[k] += price
            last_price = price
        p1 += secret

    p2 = max(counter.values())
    return f"Part 1: {p1}, Part 2: {p2}"
