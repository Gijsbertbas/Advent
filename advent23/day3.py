import re
import os
from aocd.models import Puzzle
import click
from dataclasses import dataclass


@dataclass
class Number:
    number: int
    start_index: int
    end_index: int

    @property
    def lookup_start(self):
        return max(0, self.start_index - 1)

    @property
    def lookup_end(self):
        return self.end_index + 1

    def is_valid(self, specials: list):
        for special in specials:
            if self.lookup_start <= special < self.lookup_end:
                return True
        return False

    def is_within(self, index: int):
        return self.lookup_start <= index < self.lookup_end


@dataclass
class Special:
    character: str
    index: int


class Line:
    numbers = []
    specials = []

    def __init__(self, line: str):
        self.line = line
        self.numbers = self._parse_numbers()
        self.specials = self._parse_specials()

    def _parse_numbers(self):
        numbers = []
        for match in re.finditer(r"(\d+)", self.line):
            numbers.append(Number(int(match.groups()[0]), match.start(), match.end()))
        return numbers

    def _parse_specials(self):
        specials = []
        for match in re.finditer(r"[^\d|\.]", self.line):
            specials.append(Special(match.group(), match.start()))
        return specials


class Schematic:
    lines = []

    def __init__(self, lines):
        self.lines = lines

    @classmethod
    def from_input(cls, input):
        return cls([Line(line) for line in input.splitlines()])

    def sum_of_valid_numbers(self):
        solution = 0
        for i, line in enumerate(self.lines):
            specials = []
            specials = [s.index for s in line.specials]
            specials.extend([s.index for s in self.lines[max(i - 1, 0)].specials])
            specials.extend(
                [s.index for s in self.lines[min(i + 1, len(self.lines) - 1)].specials]
            )
            for number in line.numbers:
                if number.is_valid(specials):
                    solution += number.number
        return solution

    def sum_of_gears(self):
        solution = 0
        for i, line in enumerate(self.lines):
            for special in line.specials:
                if special.character == "*":
                    numbers = [n for n in line.numbers if n.is_within(special.index)]
                    numbers.extend(
                        [
                            n
                            for n in self.lines[max(i - 1, 0)].numbers
                            if n.is_within(special.index)
                        ]
                    )
                    numbers.extend(
                        [
                            n
                            for n in self.lines[min(i + 1, len(self.lines) - 1)].numbers
                            if n.is_within(special.index)
                        ]
                    )
                    if len(numbers) == 2:
                        solution += numbers[0].number * numbers[1].number
        return solution


def first(input) -> int:
    schematic = Schematic.from_input(input)
    return schematic.sum_of_valid_numbers()


def second(input) -> int:
    schematic = Schematic.from_input(input)
    return schematic.sum_of_gears()


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
