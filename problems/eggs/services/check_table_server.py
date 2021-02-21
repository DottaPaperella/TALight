#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="check_table"
args_list = [
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit, argv
from random import randrange
from math import inf as IMPOSSIBLE

from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

print('# waiting for a rectangular table of natural numbers. Insert line "# END" to close the table.')
def get_line():
    raw_line = input().strip()
    if raw_line[0] != "#":
        return raw_line.split("#")[0].split(), None
    key = raw_line[1:].strip().split()[0].upper()
    if key == "END" or key == "NEXT":
        return None, key 
    return None, "GEN_COMMENT"

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False    

first_line, cmd = get_line() 
while first_line == None:
    first_line, cmd = get_line()

last_floor = len(first_line)
table_submitted = [ [0] + [IMPOSSIBLE] * last_floor ]

if not all(represents_int(_) for _ in first_line):
    print(f"# Error (in the table format): All entries in your table should be integers. Just checked your first row.")
    exit(1)
table_submitted.append([0] + list(map(int, first_line)))

next_line, cmd = get_line() 
while cmd != "END":
    if cmd == "NEXT":
        print("# Error: This service does not accept more than one single table.")
        exit(1)
    if next_line != None:
        if not all(represents_int(_) for _ in next_line):
            print(f"# Error (in the table format): All entries in your table should be integers. Just check row {len(table_submitted)} in your file.")
            exit(1)
        if len(next_line) != last_floor:
            print(f"# Error (in the table format): The row {len(table_submitted)} of your table contains {len(next_line)} integers whereas all previous rows contain {last_floor} integers.")
            exit(1)
        table_submitted.append([0] + list(map(int,next_line)))
    next_line, cmd = get_line()
print("# FILE GOT")

def entry_should_be(n_eggs,n_floors):
    if n_floors == 0:
        return 0
    if n_eggs == 0:
        return IMPOSSIBLE
    risp = IMPOSSIBLE
    for first_launch_floor in range(1,1+n_floors):
        risp = min(risp,1+max(table_submitted[n_eggs][n_floors-first_launch_floor],table_submitted[n_eggs-1][first_launch_floor-1]))
    return risp

def check_entry(n_eggs,n_floors):
    if table_submitted[n_eggs][n_floors] != entry_should_be(n_eggs,n_floors):
        print(f"! We disagree: according to your table, you need {table_submitted[n_eggs][n_floors]} launches when given {n_eggs} eggs and {n_floors} floors. In our opinion the minimum number of launches needed in the worst case is {entry_should_be(n_eggs,n_floors)}.")
        exit(0)

for n_eggs in range(len(table_submitted)):
    for n_floors in range(len(table_submitted[0])):
        check_entry(n_eggs,n_floors)

print(f"Ok! Your table is correct in every single entry!")

exit(0)