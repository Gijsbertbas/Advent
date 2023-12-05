from datetime import datetime
from aocd.models import Puzzle
from collections import Counter
puzzle = Puzzle(year=2021, day=14)
data = puzzle.input_data.split("\n")

example_data = [line.strip() for line in open('day14.example.input').readlines()]

def interpret_data(data: list) -> tuple:
    template = data[0]
    rules = {}
    for line in data[2:]:
        rule = line.split(' -> ')
        rules[rule[0]] = rule[1]
    return template, rules

def step(template: str, rules: dict) -> str:
    blocks = []
    for i in range(len(template)-1):
        pair = template[i:i+2]
        blocks.append(pair[0] + rules[pair] + pair[1])
    template = blocks[0]
    return template + ''.join([b[1:] for b in blocks[1:]])
    
def solve(data: list, steps: int = 10) -> int:
    template, rules = interpret_data(data)
    for s in range(steps):
        print(f"Running step: {s+1}...")
        template = step(template, rules)
        print(f"Resulting template has length {len(template)}")
        write_template(template)
        print("Template written to file")
    c = Counter(template).values()
    return max(c) - min(c)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def solve2(data: list, steps: int = 10, chunklength = 100000) -> int:
    template, rules = interpret_data(data)
    for s in range(steps):
        print(f"Running step: {s+1}...")
        start = datetime.now()
        parts = []
        for chunk in chunks(template, chunklength):
            parts.append(step(chunk, rules))
        template = parts[0]
        for i, part in enumerate(parts[1:]):
            template += rules[parts[i][-1] + parts[i+1][0]]
            template += part            
        timepassed = datetime.now()-start
        print(f"Step took {timepassed.seconds} seconds")
        write_template(template)
        print("Template written to file")
    c = Counter(template).values()
    return max(c) - min(c)

def write_template(template: str):
    with open('template.txt', 'w') as f:
        f.write(template)

if __name__ == "__main__":
    result = solve2(example_data, 40)
    print(f"Finished, solution = {result}")
