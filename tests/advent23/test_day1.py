from advent23.day1 import first, second


example1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def test_first():
    assert first(example1) == 142


example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def test_second():
    assert second(example2) == 281
