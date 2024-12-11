from collections import Counter

example: str = "125 17"

def parse(input: str) -> dict[int, int]:
    return Counter(int(w) for w in input.split())

def blink(stones: dict[int, int]) -> dict[int, int]:
    after = {}
    for stone, count in stones.items():
        digits = str(stone)
        if stone == 0: # replace them all with 1s
            after[1] = after.get(1, 0) + count
        elif len(digits) % 2 == 0:
            left, right = int(digits[:len(digits) // 2]), int(digits[len(digits) // 2:])
            after[left] = after.get(left, 0) + count
            after[right] = after.get(right, 0) + count
        else:
            after[stone * 2024] = after.get(stone * 2024, 0) + count
    return after

def main(input: str) -> str:
    stones = parse(input)
    for _ in range(25):
        stones = blink(stones)
    p1 = sum(count for count in stones.values())
    for _ in range(50):
        stones = blink(stones)
    p2 = sum(count for count in stones.values())
    return f"Part 1: {p1}, Part 2: {p2}"

if __name__ == '__main__':
    print(main(example))
