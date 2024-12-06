example: str = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def main(input: str) -> str:
    grid = [line.strip() for line in input.splitlines()]
    H, W = len(grid), len(grid[0])
    dirs = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    seen, mas = 0, 0
    for y in range(H):
        for x in range(W):
            for dx, dy in dirs:
                w = ""
                for i in range(4):
                    (xp, yp) = (x + dx * i, y + dy * i)
                    if 0 <= xp < W and 0 <= yp < H:
                        w += grid[yp][xp]
                seen += w == "XMAS"
            left, right = "", ""
            for i in range(3):
                xp, yp = x + i, y + i
                if 0 <= xp < W and 0 <= yp < H:
                    right += grid[yp][xp]
                xp, yp = x + 2 - i, y + i
                if 0 <= xp < W and 0 <= yp < H:
                    left += grid[yp][xp]
            mas += left in ("MAS", "SAM") and right in ("MAS", "SAM")
    return f"Part 1: {seen}, Part 2: {mas}"


def test_day_4():
    assert main(example) == "Part 1: 18, Part 2: 9"
