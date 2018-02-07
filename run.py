import time

import math

from emulator import cyt_run, pure_run, Bytecode
from gene import World

b1 = Bytecode("++++++++[->-[->-[->-[-]<]<]<]>++++++++[<++++++++++>-]<[>+>+<<-]>-.>-----.>")
print(b1)
b2 = Bytecode("[[+]]")
print(b2)


world = World(count_genes=10)
world.print()
last = math.inf
for x in range(1000):
    _, cur = list(world.step())[0]

    print(F"==== dERROR: {last - cur} ====")
    last = cur


