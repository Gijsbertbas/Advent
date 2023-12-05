import os
import re
from aocd.models import Puzzle
import click


def first(input) -> int:
    solution = 0
    for line in input.splitlines():
        digits = re.findall(r"\d", line)
        solution += int(digits[0] + digits[-1])
    return solution


mapping = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

reversemapping = {
    "eno": "1",
    "owt": "2",
    "eerht": "3",
    "ruof": "4",
    "evif": "5",
    "xis": "6",
    "neves": "7",
    "thgie": "8",
    "enin": "9",
}


def second(input) -> int:
    solution = 0
    for line in input.splitlines():
        first = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", line)
        second = re.findall(
            r"(\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)", line[::-1]
        )
        solution += int(
            mapping.get(first[0], first[0]) + reversemapping.get(second[0], second[0])
        )
    return solution


@click.command()
@click.option(
    "--part",
    type=click.Choice(["1", "2"]),
    help="Which part do you want to solve?",
    prompt=True,
)
@click.option(
    "--submit", is_flag=True, default=False, help="Do you want to submit the solution?"
)
def solve(part, submit):
    day = int(re.search(r"day(\d+).py", os.path.realpath(__file__)).groups()[0])
    puzzle = Puzzle(year=2023, day=day)
    match part:
        case "1":
            solution = first(puzzle.input_data)
            if submit:
                puzzle.answer_a = solution
        case "2":
            solution = second(puzzle.input_data)
            if submit:
                puzzle.answer_b = second(puzzle.input_data)
    if not submit:
        print(f"Solution part {part}: {solution}")


if __name__ == "__main__":
    solve()
