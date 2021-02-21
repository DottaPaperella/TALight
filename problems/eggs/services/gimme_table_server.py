#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="gimme_table"
args_list = [
    ('n_eggs',int),
    ('n_floors',int),
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


# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * ENV.n_floors ]
for u in range(ENV.n_eggs):
    table.append([0] + [None] * ENV.n_floors)

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+ENV.n_eggs):
    for f in range(1,1+ENV.n_floors):
        table[u][f] = IMPOSSIBLE
        for first_launch_floor in range(1,1+f):
            table[u][f] = min(table[u][f],1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]))

# PRINTING OUT THE TABLE:
fmt = f"%{1+len(str(table[-1][-1]))}d"
for row in table[1:]:
    for ele in row[1:]:
        print(fmt % ele, end=" ")
    print()    
exit(0)