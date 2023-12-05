from advent23.day3 import first, second


example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test_first():
    assert first(example) == 4361


def test_second():
    assert second(example) == 467835
