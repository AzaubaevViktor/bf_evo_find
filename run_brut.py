from itertools import product

import sys

from emulator import Bytecode, BFError, cyt_run


parts = "+-<>[]"

COUNT_GENES = 10
MEM_SIZE = 10
MAX_CYCLES = 1000000
MAX_ERRORS = 10


# Generate values
def func(a, b):
    if b == 0:
        return 0
    return (a % b) % 256


values = []
for a in range(256):
    for b in range(256):
        values.append((a, b, func(a, b)))


# Check
success = []
iteration = 0
all_iterations = 6 ** COUNT_GENES
for code in product(*[parts for x in range(COUNT_GENES)]):
    iteration += 1

    try:
        bc = Bytecode("".join(code))
    except BFError:
        continue

    if "[]" in str(bc) or "[-]" in str(bc) or "[+]" in str(bc):
        continue

    print("\r", end="")
    sys.stdout.flush()
    print("{}/{}| ".format(iteration, all_iterations), end="")
    print(bc, end=": ")

    score = 0
    errors = 0

    for a, b, result in values:
        mem = [0] * MEM_SIZE
        mem[0] = a
        mem[1] = b

        try:
            mem = cyt_run(
                bc.bytecode,
                mem_size=MEM_SIZE,
                max_cycles=MAX_CYCLES,
                mem=mem
            )
        except BFError:
            # if long execute or go into elft, stop
            errors += MAX_ERRORS

        if result == mem[0]:
            score += 1
        else:
            errors += 1

        if errors > MAX_ERRORS:
            print("Too many errors", end="")
            break

    if errors > MAX_ERRORS:
        continue

    print("OK! score: {}".format(bc, score))

    success.append(
        (bc, score)
    )

print()
print("Successes:")
for bc, score in success:
    print(bc, score)
