import re
import os
from aocd.models import Puzzle
import click


def passes(round) -> bool:
    reds = re.search(r"(\d+) red", round)
    if reds and int(reds.groups()[0]) > 12:
        return False
    greens = re.search(r"(\d+) green", round)
    if greens and int(greens.groups()[0]) > 13:
        return False
    blues = re.search(r"(\d+) blue", round)
    if blues and int(blues.groups()[0]) > 14:
        return False
    return True


def first(input) -> int:
    """12 red cubes, 13 green cubes, and 14 blue cubes"""
    solution = 0
    for line in input.splitlines():
        game_id = int(re.search(r"Game (\d+):", line).groups()[0])
        if all((passes(round) for round in line.split(";"))):
            solution += game_id
    return solution


def power(line) -> int:
    reds = re.findall(r"(\d+) red", line)
    greens = re.findall(r"(\d+) green", line)
    blues = re.findall(r"(\d+) blue", line)
    return (
        max((int(red) for red in reds))
        * max((int(green) for green in greens))
        * max((int(blue) for blue in blues))
    )


def second(input) -> int:
    solution = 0
    for line in input.splitlines():
        solution += power(line)
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
