from typing import TypeAlias

example: str = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

Pos: TypeAlias = tuple[int, int]
Walls: TypeAlias = set[Pos]
Boxes: TypeAlias = set[Pos]


def parse(inp: str) -> tuple[Walls, Boxes, str, Pos]:
    warehouse, instructions = inp.split("\n\n")
    walls: Walls = set()
    boxes: Boxes = set()
    bot = (0, 0)
    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
            elif c == "O":
                boxes.add((x, y))
            elif c == "@":
                bot = (x, y)
    assert bot != (0, 0)
    return walls, boxes, instructions.replace("\n", ""), bot


def parse_wide(inp: str) -> tuple[Walls, Boxes, str, Pos]:
    walls, boxes, instructions, bot = parse(inp)
    boxes = {(x * 2, y) for x, y in boxes}
    extended_walls = set()
    for x, y in walls:
        extended_walls.add((2 * x, y))
        extended_walls.add((2 * x + 1, y))
    return extended_walls, boxes, instructions, (bot[0] * 2, bot[1])


def gps_score(boxes: Boxes) -> int:
    return sum(y * 100 + x for x, y in boxes)


def shift(p: Pos, direction: str) -> Pos:
    assert direction in "^v<>^"
    x, y = p
    if direction == "^":
        return x, y - 1
    elif direction == "v":
        return x, y + 1
    elif direction == ">":
        return x + 1, y
    else:
        return x - 1, y


def move_bot_small_warehouse(
    bot: Pos, direction: str, walls: Walls, boxes: Boxes
) -> Pos:
    next = shift(bot, direction)

    if next in walls:
        return bot
    elif next not in boxes:
        return next

    while next in boxes:
        next = shift(next, direction)

    if next not in boxes and next not in walls:
        bot = shift(bot, direction)
        boxes.remove(bot)
        boxes.add(next)
        return bot
    else:
        return bot


def small_warehouse(inp: str) -> int:
    walls, boxes, instructions, bot = parse(inp)
    for direction in instructions:
        bot = move_bot_small_warehouse(bot, direction, walls, boxes)
    return gps_score(boxes)


def move_bot_wide_warehouse(
    bot: Pos, direction: str, walls: Walls, boxes: Boxes
) -> Pos:
    next = shift(bot, direction)

    if next in walls:
        return bot

    move_boxes = set()
    work = []

    match direction:
        case "<":
            left = shift(next, "<")
            if left in boxes:
                work.append(left)
            while True:
                if not work:
                    break
                box = work.pop()
                one_left = shift(box, "<")
                if one_left in walls:
                    return bot
                move_boxes.add(box)
                neighbour = shift(one_left, "<")
                if neighbour in boxes:
                    work.append(neighbour)
        case ">":
            if next in boxes:
                work.append(next)
            while True:
                if not work:
                    break
                box = work.pop()
                next_pos = shift(box, ">")
                if shift(next_pos, ">") in walls:
                    return bot
                move_boxes.add(box)
                neighbour = shift(next_pos, ">")
                if neighbour in boxes:
                    work.append(neighbour)
        case "^" | "v":
            if next in boxes:
                work.append(next)
            elif shift(next, "<") in boxes:
                work.append(shift(next, "<"))

            while True:
                if not work:
                    break
                box = work.pop()
                move_boxes.add(box)
                next_pos = shift(box, direction)
                if next_pos in walls or shift(next_pos, ">") in walls:
                    return bot
                if next_pos in boxes:
                    work.append(next_pos)
                else:
                    if shift(next_pos, ">") in boxes:
                        work.append(shift(next_pos, ">"))
                    if shift(next_pos, "<") in boxes:
                        work.append(shift(next_pos, "<"))
    assert all(box in boxes for box in move_boxes)
    boxes.difference_update(move_boxes)
    boxes.update({shift(box, direction) for box in move_boxes})
    return next


def wide_warehouse(inp: str) -> int:
    walls, boxes, instructions, bot = parse_wide(inp)
    for direction in instructions:
        bot = move_bot_wide_warehouse(bot, direction, walls, boxes)
    return gps_score(boxes)


def main(inp: str) -> str:
    return f"Part 1: {small_warehouse(inp)}, Part 2: {wide_warehouse(inp)}"


def test_parse():
    small = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
    walls, boxes, instructions, bot = parse(small)
    assert instructions == "<^^>>>vv<v>>v<<"
    assert (0, 0) in walls
    assert bot == (2, 2)
    assert len(boxes) == 6
    walls, boxes, instructions, bot = parse_wide(small)
    assert len(boxes) == 6


def test_small_warehouse():
    assert small_warehouse(example) == 10092
